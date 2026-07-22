# -*- coding: utf-8 -*-
"""Warstwa abstrakcji repozytorium (Konstytucja Techniczna, sekcja III).
Rdzeń nie wie, czy pod spodem jest SQLite czy PostgreSQL.
Zmiana silnika = podmiana implementacji tej klasy, bez dotykania parsera i logiki.
Indeks jest POCHODNY i odtwarzalny (sekcja II): rebuild() kasuje i buduje od zera z plików.
"""
from abc import ABC, abstractmethod
import sqlite3, json

SCHEMA_VERSION = "0.1"  # wersja schematu grafu (Konstytucja, sekcja IX)

class RepozytoriumIndeksu(ABC):
    """Kontrakt, który zna rdzeń. Silnik jest szczegółem implementacyjnym."""
    @abstractmethod
    def rebuild(self): ...
    @abstractmethod
    def close(self): ...
    @abstractmethod
    def dodaj_wezel(self, wezel: dict): ...
    @abstractmethod
    def dodaj_krawedz(self, zrodlo: str, cel: str, typ: str): ...
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
        # siatka bezpieczeństwa, gdyby ktoś zapomniał close()/with
        try:
            self.close()
        except Exception:
            pass

    def rebuild(self):
        c = self.db
        c.executescript("""
        DROP TABLE IF EXISTS wezly;
        DROP TABLE IF EXISTS krawedzie;
        DROP TABLE IF EXISTS meta;
        CREATE TABLE wezly (
            id TEXT PRIMARY KEY, typ TEXT, tytul TEXT,
            status_epistemiczny TEXT, wersja TEXT, dane_json TEXT
        );
        CREATE TABLE krawedzie (
            zrodlo TEXT, cel TEXT, typ TEXT
        );
        CREATE TABLE meta (klucz TEXT PRIMARY KEY, wartosc TEXT);
        """)
        c.execute("INSERT INTO meta VALUES ('schema_version', ?)", (SCHEMA_VERSION,))
        c.commit()

    def dodaj_wezel(self, w):
        self.db.execute(
            "INSERT OR REPLACE INTO wezly VALUES (?,?,?,?,?,?)",
            (w['id'], w.get('typ',''), w.get('tytul',''),
             w.get('status_epistemiczny',''), w.get('wersja',''),
             json.dumps(w, ensure_ascii=False)))
        self.db.commit()

    def dodaj_krawedz(self, zrodlo, cel, typ):
        self.db.execute("INSERT INTO krawedzie VALUES (?,?,?)", (zrodlo, cel, typ))
        self.db.commit()

    def wezel(self, ident):
        r = self.db.execute("SELECT dane_json FROM wezly WHERE id=?", (ident,)).fetchone()
        return json.loads(r['dane_json']) if r else None

    def wszystkie_wezly(self):
        return [json.loads(r['dane_json'])
                for r in self.db.execute("SELECT dane_json FROM wezly")]

    def krawedzie_z(self, ident):
        return [dict(r) for r in self.db.execute(
            "SELECT zrodlo,cel,typ FROM krawedzie WHERE zrodlo=?", (ident,))]

    def martwe_krawedzie(self):
        """Krawędź wskazująca na nieistniejący węzeł. Czujnik integralności grafu."""
        return [dict(r) for r in self.db.execute("""
            SELECT k.zrodlo, k.cel, k.typ FROM krawedzie k
            LEFT JOIN wezly w ON k.cel = w.id
            WHERE w.id IS NULL
        """)]
