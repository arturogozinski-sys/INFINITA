# -*- coding: utf-8 -*-
"""Warstwa abstrakcji repozytorium (Konstytucja Techniczna, sekcja III).
Rdzeń nie wie, czy pod spodem jest SQLite czy PostgreSQL.
Zmiana silnika = podmiana implementacji tej klasy, bez dotykania parsera i logiki.
Indeks jest POCHODNY i odtwarzalny (sekcja II): pełna wymiana powstaje z plików.
"""
from abc import ABC, abstractmethod
import json
import sqlite3


class RepozytoriumIndeksu(ABC):
    """Kontrakt, który zna rdzeń. Silnik jest szczegółem implementacyjnym.
    Wersja schematu NIE jest stałą w kodzie — jedynym źródłem jest schemat_grafu.json.
    """

    @abstractmethod
    def rebuild(self): ...

    @abstractmethod
    def close(self): ...

    @abstractmethod
    def dodaj_wezel(self, wezel: dict): ...

    @abstractmethod
    def dodaj_krawedz(self, zrodlo: str, cel: str, typ: str): ...

    @abstractmethod
    def ustaw_wersje_schematu(self, wersja: str): ...

    @abstractmethod
    def zamien_wszystko_atomowo(self, wezly: list, krawedzie: list, wersja_schematu: str): ...

    @abstractmethod
    def wezel(self, ident: str) -> dict | None: ...

    @abstractmethod
    def wszystkie_wezly(self) -> list: ...

    @abstractmethod
    def krawedzie_z(self, ident: str) -> list: ...

    @abstractmethod
    def martwe_krawedzie(self) -> list: ...


class IndeksSQLite(RepozytoriumIndeksu):
    """Implementacja na SQLite. Wymienialna. Postgres = inna klasa, ten sam kontrakt."""

    def __init__(self, sciezka=":memory:"):
        self.db = sqlite3.connect(sciezka)
        self.db.row_factory = sqlite3.Row

    def close(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    @staticmethod
    def _utworz_tabele(cursor):
        """DDL wykonywany pojedynczymi poleceniami, bez executescript().
        executescript() może niejawnie zatwierdzać transakcję, więc nie nadaje się
        do atomowej wymiany indeksu.
        """
        cursor.execute("DROP TABLE IF EXISTS wezly")
        cursor.execute("DROP TABLE IF EXISTS krawedzie")
        cursor.execute("DROP TABLE IF EXISTS meta")
        cursor.execute("""
            CREATE TABLE wezly (
                id TEXT PRIMARY KEY,
                typ TEXT,
                tytul TEXT,
                status_epistemiczny TEXT,
                wersja TEXT,
                dane_json TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE krawedzie (
                zrodlo TEXT,
                cel TEXT,
                typ TEXT
            )
        """)
        cursor.execute("CREATE TABLE meta (klucz TEXT PRIMARY KEY, wartosc TEXT)")

    def rebuild(self):
        """Jawna, samodzielna inicjalizacja pustego indeksu.
        Produkcyjna budowa używa zamien_wszystko_atomowo().
        """
        cursor = self.db.cursor()
        self._utworz_tabele(cursor)
        self.db.commit()

    def ustaw_wersje_schematu(self, wersja):
        self.db.execute(
            "INSERT OR REPLACE INTO meta VALUES ('schema_version', ?)",
            (wersja,),
        )
        self.db.commit()

    def dodaj_wezel(self, w):
        """Zwykły INSERT — duplikat ID ma wybuchnąć, nie zostać nadpisany."""
        self.db.execute(
            "INSERT INTO wezly VALUES (?,?,?,?,?,?)",
            (
                w['id'],
                w.get('typ', ''),
                w.get('tytul', ''),
                w.get('status_epistemiczny', ''),
                w.get('wersja', ''),
                json.dumps(w, ensure_ascii=False),
            ),
        )
        self.db.commit()

    def dodaj_krawedz(self, zrodlo, cel, typ):
        self.db.execute(
            "INSERT INTO krawedzie VALUES (?,?,?)",
            (zrodlo, cel, typ),
        )
        self.db.commit()

    def zamien_wszystko_atomowo(self, wezly, krawedzie, wersja_schematu):
        """Atomowo zastępuje cały indeks.

        SAVEPOINT obejmuje usunięcie starego schematu, utworzenie tabel i wszystkie
        inserty. Dowolny wyjątek podczas DDL, serializacji albo zapisu cofa CAŁĄ
        wymianę i pozostawia poprzedni indeks bez zmian.
        """
        cursor = self.db.cursor()
        cursor.execute("SAVEPOINT wymiana_indeksu")
        try:
            self._utworz_tabele(cursor)
            cursor.execute(
                "INSERT INTO meta VALUES ('schema_version', ?)",
                (wersja_schematu,),
            )
            for w in wezly:
                cursor.execute(
                    "INSERT INTO wezly VALUES (?,?,?,?,?,?)",
                    (
                        w['id'],
                        w.get('typ', ''),
                        w.get('tytul', ''),
                        w.get('status_epistemiczny', ''),
                        w.get('wersja', ''),
                        json.dumps(w, ensure_ascii=False),
                    ),
                )
            for zrodlo, cel, typ in krawedzie:
                cursor.execute(
                    "INSERT INTO krawedzie VALUES (?,?,?)",
                    (zrodlo, cel, typ),
                )
            cursor.execute("RELEASE SAVEPOINT wymiana_indeksu")
        except Exception:
            cursor.execute("ROLLBACK TO SAVEPOINT wymiana_indeksu")
            cursor.execute("RELEASE SAVEPOINT wymiana_indeksu")
            raise

    def wezel(self, ident):
        r = self.db.execute(
            "SELECT dane_json FROM wezly WHERE id=?",
            (ident,),
        ).fetchone()
        return json.loads(r['dane_json']) if r else None

    def wszystkie_wezly(self):
        return [
            json.loads(r['dane_json'])
            for r in self.db.execute("SELECT dane_json FROM wezly")
        ]

    def krawedzie_z(self, ident):
        return [
            dict(r)
            for r in self.db.execute(
                "SELECT zrodlo,cel,typ FROM krawedzie WHERE zrodlo=?",
                (ident,),
            )
        ]

    def martwe_krawedzie(self):
        """Krawędź wskazująca na nieistniejący węzeł. Czujnik integralności grafu."""
        return [
            dict(r)
            for r in self.db.execute("""
                SELECT k.zrodlo, k.cel, k.typ
                FROM krawedzie k
                LEFT JOIN wezly w ON k.cel = w.id
                WHERE w.id IS NULL
            """)
        ]
