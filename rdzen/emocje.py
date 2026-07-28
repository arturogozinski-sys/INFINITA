# -*- coding: utf-8 -*-
"""Wykonywalna projekcja zamrożonego filtra emocji.

Moduł przyjmuje wyłącznie dane już przetłumaczone na wartości kategorialne.
Nie tłumaczy narracji, nie diagnozuje i nie rozstrzyga trafności biologicznej.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path


LICZBA_WYMIAROW = 12
LICZBA_RODZIN = 14
STATUSY_DOMKNIECIA = {"zgodne", "sprzeczne", "nieokreslone"}


class BladModeluEmocji(ValueError):
    pass


def _wczytaj_json(sciezka: Path) -> dict:
    with sciezka.open(encoding="utf-8") as plik:
        return json.load(plik)


def _warunki_wyrazenia(wyrazenie: dict):
    if "warunek" in wyrazenie:
        yield wyrazenie["warunek"]
        return
    for klucz in ("wszystkie", "dowolny"):
        if klucz in wyrazenie:
            for element in wyrazenie[klucz]:
                yield from _warunki_wyrazenia(element)
            return
    raise BladModeluEmocji(f"Nieznany typ wyrażenia: {wyrazenie!r}")


def waliduj_model(model: dict) -> None:
    wymiary = model.get("wymiary", {})
    rodziny = model.get("rodziny", {})
    if len(wymiary) != LICZBA_WYMIAROW:
        raise BladModeluEmocji(
            f"Model ma {len(wymiary)} wymiarów zamiast {LICZBA_WYMIAROW}."
        )
    if len(rodziny) != LICZBA_RODZIN:
        raise BladModeluEmocji(
            f"Model ma {len(rodziny)} rodzin zamiast {LICZBA_RODZIN}."
        )

    for wymiar, wartosci in wymiary.items():
        if not wartosci or len(wartosci) != len(set(wartosci)):
            raise BladModeluEmocji(f"Niepoprawny słownik wymiaru {wymiar}.")
        if not any(wartosc.startswith("nieokresl") for wartosc in wartosci):
            raise BladModeluEmocji(f"Wymiar {wymiar} nie ma wartości nieokreślonej.")

    kierunki = set(wymiary["kierunek_dzialania"])
    for rodzina, definicja in rodziny.items():
        for warunek in _warunki_wyrazenia(definicja["warunki_konieczne"]):
            wymiar = warunek["wymiar"]
            if wymiar not in wymiary:
                raise BladModeluEmocji(
                    f"Rodzina {rodzina} używa nieznanego wymiaru {wymiar}."
                )
            nieznane = set(warunek["jedna_z"]) - set(wymiary[wymiar])
            if nieznane:
                raise BladModeluEmocji(
                    f"Rodzina {rodzina} używa nieznanych wartości: {sorted(nieznane)}."
                )
        nieznane_kierunki = set(definicja["kierunki_dzialania"]) - kierunki
        if nieznane_kierunki:
            raise BladModeluEmocji(
                f"Rodzina {rodzina} używa nieznanych kierunków: "
                f"{sorted(nieznane_kierunki)}."
            )
        if set(definicja["domkniecie"]) != {"wygasanie", "utrwalanie"}:
            raise BladModeluEmocji(f"Rodzina {rodzina} ma niepełne domknięcie.")
        if "warunki_wykluczajace" in definicja:
            raise BladModeluEmocji(
                f"Rodzina {rodzina} uruchamia nieaktywny warunek wykluczający."
            )


def _normalizuj_dane(model: dict, dane: dict) -> dict[str, set[str]]:
    wynik: dict[str, set[str]] = {}
    nieznane_wymiary = set(dane) - set(model["wymiary"])
    if nieznane_wymiary:
        raise BladModeluEmocji(
            f"Nieznane wymiary wejścia: {sorted(nieznane_wymiary)}."
        )

    for wymiar, podane in dane.items():
        if isinstance(podane, str):
            wartosci = {podane}
        else:
            wartosci = set(podane)
        if not wartosci:
            raise BladModeluEmocji(f"Wymiar {wymiar} ma pusty zbiór.")
        nieznane = wartosci - set(model["wymiary"][wymiar])
        if nieznane:
            raise BladModeluEmocji(
                f"Wymiar {wymiar} ma nieznane wartości: {sorted(nieznane)}."
            )
        nieokreslone = {
            wartosc for wartosc in wartosci if wartosc.startswith("nieokresl")
        }
        if nieokreslone and len(wartosci) > 1:
            raise BladModeluEmocji(
                f"Wymiar {wymiar} łączy wartość nieokreśloną z określoną."
            )
        wynik[wymiar] = wartosci
    return wynik


def _spelnia(wyrazenie: dict, dane: dict[str, set[str]]) -> bool:
    if "warunek" in wyrazenie:
        warunek = wyrazenie["warunek"]
        obecne = dane.get(warunek["wymiar"], set())
        return bool(obecne.intersection(warunek["jedna_z"]))
    if "wszystkie" in wyrazenie:
        return all(_spelnia(element, dane) for element in wyrazenie["wszystkie"])
    if "dowolny" in wyrazenie:
        return any(_spelnia(element, dane) for element in wyrazenie["dowolny"])
    raise BladModeluEmocji(f"Nieznany typ wyrażenia: {wyrazenie!r}")


@dataclass(frozen=True)
class WynikDekodera:
    wynik: str
    kandydaci: tuple[str, ...]
    po_syntezie: tuple[str, ...]
    po_tescie_dzialania: tuple[str, ...]
    ocena_domkniecia_wymagana: bool

    def jako_slownik(self) -> dict:
        return {
            "wynik": self.wynik,
            "kandydaci": list(self.kandydaci),
            "po_syntezie": list(self.po_syntezie),
            "po_tescie_dzialania": list(self.po_tescie_dzialania),
            "ocena_domkniecia_wymagana": self.ocena_domkniecia_wymagana,
        }


class DekoderEmocji:
    def __init__(self, model: dict):
        waliduj_model(model)
        self.model = model

    @classmethod
    def z_aktywnej_wersji(cls, katalog_repo: str | Path) -> "DekoderEmocji":
        katalog_repo = Path(katalog_repo)
        wskaznik = _wczytaj_json(
            katalog_repo / "systemy" / "emocje" / "AKTYWNA_WERSJA.json"
        )
        model = _wczytaj_json(katalog_repo / wskaznik["model_wykonawczy"])
        return cls(model)

    def dekoduj(
        self,
        dane: dict,
        zgodnosc_domkniecia: dict[str, str] | None = None,
    ) -> WynikDekodera:
        """Klasyfikuje dane kategorialne.

        `zgodnosc_domkniecia` jest wynikiem odrębnej analizy tekstowej wymaganej
        przez dokument źródłowy. Brak tej mapy nie odrzuca kandydatów.
        """
        dane = _normalizuj_dane(self.model, dane)

        po_syntezie = {
            rodzina
            for rodzina, definicja in self.model["rodziny"].items()
            if _spelnia(definicja["warunki_konieczne"], dane)
        }

        kierunki = dane.get("kierunek_dzialania", set())
        kierunek_nieokreslony = not kierunki or "nieokreslony" in kierunki
        po_dzialaniu = {
            rodzina
            for rodzina in po_syntezie
            if kierunek_nieokreslony
            or kierunki.intersection(
                self.model["rodziny"][rodzina]["kierunki_dzialania"]
            )
        }

        domkniecie = dane.get("warunek_domkniecia", set())
        domkniecie_okreslone = bool(
            domkniecie and "nieokreslony" not in domkniecie
        )
        if zgodnosc_domkniecia is None:
            zgodnosc_domkniecia = {}
        for rodzina, status in zgodnosc_domkniecia.items():
            if rodzina not in self.model["rodziny"]:
                raise BladModeluEmocji(
                    f"Ocena domknięcia dotyczy nieznanej rodziny {rodzina}."
                )
            if status not in STATUSY_DOMKNIECIA:
                raise BladModeluEmocji(
                    f"Nieznany status domknięcia {status} dla {rodzina}."
                )

        po_domknieciu = {
            rodzina
            for rodzina in po_dzialaniu
            if zgodnosc_domkniecia.get(rodzina, "nieokreslone") != "sprzeczne"
        }
        kandydaci = tuple(sorted(po_domknieciu))
        if len(kandydaci) == 1:
            wynik = kandydaci[0]
        elif kandydaci:
            wynik = "nierozstrzygniety_konflikt_kandydatow"
        else:
            wynik = "nierozstrzygniety_brak_pasujacej_rodziny"

        wymaga_oceny = bool(
            domkniecie_okreslone
            and any(
                rodzina not in zgodnosc_domkniecia
                for rodzina in po_dzialaniu
            )
        )
        return WynikDekodera(
            wynik=wynik,
            kandydaci=kandydaci,
            po_syntezie=tuple(sorted(po_syntezie)),
            po_tescie_dzialania=tuple(sorted(po_dzialaniu)),
            ocena_domkniecia_wymagana=wymaga_oceny,
        )


def sprawdz_manifest(katalog_repo: str | Path) -> list[str]:
    katalog_repo = Path(katalog_repo)
    wskaznik = _wczytaj_json(
        katalog_repo / "systemy" / "emocje" / "AKTYWNA_WERSJA.json"
    )
    manifest = katalog_repo / wskaznik["manifest"]
    bledy = []
    with manifest.open(encoding="utf-8") as plik:
        for numer, wiersz in enumerate(plik, start=1):
            wiersz = wiersz.rstrip("\n")
            if not wiersz:
                continue
            try:
                oczekiwany, sciezka = wiersz.split("  ", 1)
            except ValueError:
                bledy.append(f"Wiersz {numer}: niepoprawny format.")
                continue
            plik_docelowy = katalog_repo / sciezka
            if not plik_docelowy.is_file():
                bledy.append(f"Brak pliku: {sciezka}.")
                continue
            faktyczny = hashlib.sha256(plik_docelowy.read_bytes()).hexdigest()
            if faktyczny != oczekiwany:
                bledy.append(f"Niezgodny skrót: {sciezka}.")
    return bledy
