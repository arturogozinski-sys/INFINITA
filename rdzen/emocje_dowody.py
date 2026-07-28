# -*- coding: utf-8 -*-
"""Składniowy adapter zamkniętych dowodów walidacji emocji.

Adapter czyta wyłącznie jawne pola rekordów. Zachowuje ich literalny zapis,
nie tłumaczy narracji i nie ocenia semantycznej zgodności domknięcia.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import unicodedata


POLA = {
    "przedmiot oceny": "przedmiot_oceny",
    "sprawstwo": "sprawstwo",
    "czas": "czas",
    "struktura relacji": "struktura_relacji",
    "zgodnosc z przewidywaniem": "zgodnosc_z_przewidywaniem",
    "wplyw": "wplyw",
    "mozliwosc kontroli": "mozliwosc_kontroli",
    "zakres przypisania": "zakres_przypisania",
    "ocena intencji": "ocena_intencji",
    "stabilnosc oceny": "stabilnosc_oceny",
    "kierunek dzialania": "kierunek_dzialania",
    "domkniecie": "warunek_domkniecia",
}

WARTOSCI = {
    "przedmiot_oceny": {
        "wlasne ja": ("wlasne_ja",),
        "wlasne dzialanie": ("wlasne_dzialanie",),
        "wlasna grupa": ("wlasna_grupa",),
        "inna osoba": ("inna_osoba",),
        "relacja": ("relacja",),
        "zasob lub pozycja": ("zasob_lub_pozycja",),
        "stan organizmu": ("stan_organizmu",),
        "zdarzenie": ("zdarzenie",),
        "przewidywanie": ("przewidywanie",),
        "nieokreslony": ("nieokreslony",),
    },
    "sprawstwo": {
        "wlasne": ("wlasne",),
        "wlasnej grupy": ("wlasnej_grupy",),
        "innej osoby": ("innej_osoby",),
        "okolicznosci zewnetrznych": ("okolicznosci_zewnetrznych",),
        "nieokreslone": ("nieokreslone",),
    },
    "czas": {
        "aktualny": ("aktualne",),
        "dokonany": ("dokonane",),
        "przewidywany": ("przewidywane",),
        "nieokreslony": ("nieokreslony",),
    },
    "struktura_relacji": {
        "brak lub nieistotna": ("brak_lub_nieistotna",),
        "porownanie spoleczne": ("porownanie_spoleczne",),
        "zagrozenie wiezi": ("zagrozenie_wiezi",),
        "interakcja spoleczna": ("interakcja_spoleczna",),
        "ekspozycja spoleczna": ("ekspozycja_spoleczna",),
        "nieokreslona": ("nieokreslona",),
    },
    "zgodnosc_z_przewidywaniem": {
        "zgodne": ("zgodne",),
        "niezgodne": ("niezgodne",),
        "brak aktywnego przewidywania": ("brak_aktywnego_przewidywania",),
        "nieokreslona": ("nieokreslona",),
    },
    "wplyw": {
        "zagrozenie bezpieczenstwa lub integralnosci": (
            "zagrozenie_bezpieczenstwa_lub_integralnosci",
        ),
        "przeszkoda w dazeniu do celu": ("przeszkoda_w_dazeniu_do_celu",),
        "utrata lub niedostepnosc": ("utrata_lub_niedostepnosc",),
        "utrata lub niedostepnosc celu, zasobu albo osoby": (
            "utrata_lub_niedostepnosc",
        ),
        "osiagniecie lub korzysc": ("osiagniecie_lub_korzysc",),
        "naruszenie normy": ("naruszenie_normy",),
        "naruszenie normy moralnej, spolecznej albo wlasnej": (
            "naruszenie_normy",
        ),
        "skazenie lub naruszenie integralnosci ciala": (
            "skazenie_lub_naruszenie_integralnosci_ciala",
        ),
        "zagrozenie wiezi": ("zagrozenie_wiezi",),
        "zagrozenie wiezi przez mozliwosc utraty, oslabienia albo zastapienia waznej relacji": (
            "zagrozenie_wiezi",
        ),
        "brak istotnego wplywu": ("brak_istotnego_wplywu",),
        "nieokreslony": ("nieokreslony",),
    },
    "mozliwosc_kontroli": {
        "mozliwa": ("mozliwa",),
        "ograniczona": ("ograniczona",),
        "brak": ("brak",),
        "nieokreslona": ("nieokreslona",),
    },
    "zakres_przypisania": {
        "czyn": ("czyn",),
        "cala osoba": ("cala_osoba",),
        "nieokreslony": ("nieokreslony",),
    },
    "ocena_intencji": {
        "pozytywna": ("pozytywna",),
        "negatywna": ("negatywna",),
        "obojetna": ("obojetna",),
        "nieokreslona": ("nieokreslona",),
    },
    "stabilnosc_oceny": {
        "stala": ("stala",),
        "zmienna": ("zmienna",),
        "nieokreslona": ("nieokreslona",),
    },
    "kierunek_dzialania": {
        "ochrona, unikanie albo ucieczka": ("ochrona", "unikanie", "ucieczka"),
        "sprzeciw, nacisk albo konfrontacja": (
            "sprzeciw",
            "nacisk",
            "konfrontacja",
        ),
        "wycofanie albo ograniczenie aktywnosci": (
            "wycofanie",
            "ograniczenie_aktywnosci",
        ),
        "podtrzymanie, powtorzenie albo eksploracja": (
            "podtrzymanie",
            "powtorzenie",
            "eksploracja",
        ),
        "odrzucenie, odsuniecie albo oczyszczenie": (
            "odrzucenie",
            "odsuniecie",
            "oczyszczenie",
        ),
        "zatrzymanie albo orientacja": ("zatrzymanie", "orientacja"),
        "ukrycie albo zmniejszenie widocznosci": (
            "ukrycie",
            "zmniejszenie_widocznosci",
        ),
        "naprawa, przeprosiny albo rekompensata": (
            "naprawa",
            "przeprosiny",
            "rekompensata",
        ),
        "korekta zachowania albo normalizacja kontaktu": (
            "korekta_zachowania",
            "normalizacja_kontaktu",
        ),
        "ujawnienie osiagniecia albo podtrzymanie standardu": (
            "ujawnienie_osiagniecia",
            "podtrzymanie_standardu",
        ),
        "uznanie, podziekowanie albo wzajemnosc": (
            "uznanie",
            "podziekowanie",
            "wzajemnosc",
        ),
        "dystans, lekcewazenie albo wykluczenie": (
            "dystans",
            "lekcewazenie",
            "wykluczenie",
        ),
        "poprawa wlasnej pozycji, zmiana dziedziny porownania albo pomniejszanie cudzej przewagi": (
            "poprawa_wlasnej_pozycji",
            "zmiana_dziedziny_porownania",
            "pomniejszanie_cudzej_przewagi",
        ),
        "ochrona wiezi, odzyskanie zaangazowania albo sprawdzenie zagrozenia": (
            "ochrona_wiezi",
            "odzyskanie_zaangazowania",
            "sprawdzenie_zagrozenia",
        ),
        "nieokreslony": ("nieokreslony",),
    },
}

RODZINY = {
    "strach": "strach",
    "zlosc": "zlosc",
    "smutek": "smutek",
    "radosc": "radosc",
    "wstret": "wstret",
    "zaskoczenie": "zaskoczenie",
    "wstyd": "wstyd",
    "poczucie winy": "poczucie_winy",
    "zazenowanie": "zazenowanie",
    "duma": "duma",
    "wdziecznosc": "wdziecznosc",
    "zawisc": "zawisc",
    "zazdrosc": "zazdrosc",
    "pogarda": "pogarda",
}

WYNIKI = {
    "nierozstrzygniety brak pasujacej rodziny": (
        "nierozstrzygniety_brak_pasujacej_rodziny"
    ),
    "nierozstrzygniety konflikt kandydatow": (
        "nierozstrzygniety_konflikt_kandydatow"
    ),
}


class BladAdapteraDowodow(ValueError):
    pass


@dataclass(frozen=True)
class RekordDowodowy:
    seria: str
    nazwa: str
    dane: dict[str, tuple[str, ...]]
    pola_surowe: tuple[str, ...]
    domkniecie_surowe: str | None
    wynik_klucza: str
    kandydaci_klucza: tuple[str, ...]
    etap_klucza: str | None
    wariant_klucza: str | None
    rodzina_badana: str | None

    def tekst_zrodlowy(self) -> str:
        return self.nazwa + "\n\n" + "\n".join(self.pola_surowe)


def _ascii(tekst: str) -> str:
    tekst = tekst.translate({322: 108, 321: 76})
    return "".join(
        znak
        for znak in unicodedata.normalize("NFKD", tekst)
        if not unicodedata.combining(znak)
    ).casefold()


def _akapity(tekst: str) -> list[list[str]]:
    return [
        [wiersz.strip() for wiersz in blok.splitlines() if wiersz.strip()]
        for blok in tekst.replace("\r\n", "\n").split("\n\n")
    ]


def _czy_pola(wiersze: list[str]) -> bool:
    return bool(wiersze) and all(
        ":" in wiersz and _ascii(wiersz.split(":", 1)[0]) in POLA
        for wiersz in wiersze
    )


def _podziel_wartosci(wartosc: str) -> list[str]:
    return [czesc.strip() for czesc in wartosc.split(" oraz ")]


def _normalizuj_pole(wymiar: str, wartosc: str) -> tuple[str, ...] | None:
    if wymiar == "warunek_domkniecia":
        uproszczona = _ascii(wartosc)
        if uproszczona == "nieokreslone":
            return ("nieokreslony",)
        if uproszczona.startswith("wygasanie:"):
            return ("wygasanie",)
        if uproszczona.startswith("utrwalanie:"):
            return ("utrwalanie",)
        return None

    wynik: list[str] = []
    for czesc in _podziel_wartosci(wartosc):
        klucz = _ascii(czesc)
        try:
            wynik.extend(WARTOSCI[wymiar][klucz])
        except KeyError as blad:
            raise BladAdapteraDowodow(
                f"Nieznana literalna wartość {wartosc!r} wymiaru {wymiar}."
            ) from blad
    return tuple(dict.fromkeys(wynik))


def _rekordy_materialu(tekst: str) -> list[tuple[str, tuple[str, ...], dict]]:
    akapity = _akapity(tekst)
    rekordy = []
    for indeks in range(len(akapity) - 1):
        naglowek = akapity[indeks]
        pola = akapity[indeks + 1]
        if len(naglowek) != 1 or not _czy_pola(pola):
            continue
        dane = {}
        domkniecie_surowe = None
        for wiersz in pola:
            etykieta, wartosc = wiersz.split(":", 1)
            wymiar = POLA[_ascii(etykieta)]
            wartosc = wartosc.strip().rstrip(".")
            znormalizowana = _normalizuj_pole(wymiar, wartosc)
            if wymiar == "warunek_domkniecia":
                domkniecie_surowe = wartosc
            if znormalizowana is not None:
                dane[wymiar] = znormalizowana
        rekordy.append(
            (
                naglowek[0],
                tuple(pola),
                {"dane": dane, "domkniecie_surowe": domkniecie_surowe},
            )
        )
    return rekordy


def _wartosc_wiersza(wiersze: list[str], etykieta: str) -> str | None:
    prefiks = _ascii(etykieta) + ":"
    for wiersz in wiersze:
        if _ascii(wiersz).startswith(prefiks):
            return wiersz.split(":", 1)[1].strip().rstrip(".")
    return None


def _normalizuj_rodzine(wartosc: str | None) -> str | None:
    if wartosc is None:
        return None
    try:
        return RODZINY[_ascii(wartosc)]
    except KeyError as blad:
        raise BladAdapteraDowodow(f"Nieznana rodzina {wartosc!r}.") from blad


def _normalizuj_wynik(wartosc: str) -> tuple[str, tuple[str, ...]]:
    czesci = wartosc.split(":", 1)
    klucz = _ascii(czesci[0].strip())
    if klucz in RODZINY:
        return RODZINY[klucz], ()
    if klucz in WYNIKI:
        kandydaci = ()
        if len(czesci) == 2:
            kandydaci = tuple(
                sorted(
                    _normalizuj_rodzine(czesc)
                    for czesc in czesci[1].strip().split(", ")
                )
            )
        return WYNIKI[klucz], kandydaci
    raise BladAdapteraDowodow(f"Nieznany wynik klucza {wartosc!r}.")


def _segmenty_klucza(tekst: str, nazwy: list[str]) -> dict[str, list[str]]:
    wiersze = tekst.splitlines()
    pozycje = []
    zbior_nazw = set(nazwy)
    for indeks, wiersz in enumerate(wiersze):
        if wiersz.strip() in zbior_nazw:
            pozycje.append((indeks, wiersz.strip()))
    if [nazwa for _, nazwa in pozycje] != nazwy:
        raise BladAdapteraDowodow("Kolejność lub kompletność klucza jest inna niż materiału.")
    segmenty = {}
    for numer, (poczatek, nazwa) in enumerate(pozycje):
        koniec = pozycje[numer + 1][0] if numer + 1 < len(pozycje) else len(wiersze)
        segmenty[nazwa] = [
            wiersz.strip() for wiersz in wiersze[poczatek + 1 : koniec]
            if wiersz.strip()
        ]
    return segmenty


def wczytaj_korpus(katalog_repo: str | Path) -> list[RekordDowodowy]:
    katalog_repo = Path(katalog_repo)
    katalog = katalog_repo / "systemy" / "emocje" / "v1.0" / "dowody" / "serie"
    rekordy: list[RekordDowodowy] = []
    for katalog_serii in sorted(katalog.iterdir()):
        material = next(katalog_serii.glob("MATERIAL_*.md"))
        klucz = next(katalog_serii.glob("KLUCZ_*.md"))
        rekordy_materialu = _rekordy_materialu(material.read_text(encoding="utf-8"))
        nazwy = [nazwa for nazwa, _, _ in rekordy_materialu]
        segmenty = _segmenty_klucza(klucz.read_text(encoding="utf-8"), nazwy)
        for nazwa, pola_surowe, zapis in rekordy_materialu:
            segment = segmenty[nazwa]
            wynik = _wartosc_wiersza(segment, "Wynik")
            if wynik is None:
                raise BladAdapteraDowodow(f"Rekord {nazwa} nie ma wyniku w kluczu.")
            kandydaci = _wartosc_wiersza(segment, "Pozostali kandydaci")
            kandydaci_norm = ()
            if kandydaci:
                kandydaci_norm = tuple(
                    sorted(
                        _normalizuj_rodzine(czesc)
                        for czesc in kandydaci.split(", ")
                    )
                )
            wynik_norm, kandydaci_inline = _normalizuj_wynik(wynik)
            if not kandydaci_norm:
                kandydaci_norm = kandydaci_inline
            etap = _wartosc_wiersza(segment, "Etap")
            etap_norm = (
                _ascii(etap.split(".", 1)[0]).replace(" ", "_")
                if etap
                else None
            )
            rekordy.append(
                RekordDowodowy(
                    seria=katalog_serii.name,
                    nazwa=nazwa,
                    dane=zapis["dane"],
                    pola_surowe=pola_surowe,
                    domkniecie_surowe=zapis["domkniecie_surowe"],
                    wynik_klucza=wynik_norm,
                    kandydaci_klucza=kandydaci_norm,
                    etap_klucza=etap_norm,
                    wariant_klucza=_wartosc_wiersza(segment, "Wariant"),
                    rodzina_badana=_normalizuj_rodzine(
                        _wartosc_wiersza(segment, "Rodzina badana")
                    ),
                )
            )
    return rekordy


def etap_wyniku(wynik) -> str | None:
    if wynik.wynik != "nierozstrzygniety_brak_pasujacej_rodziny":
        return None
    if not wynik.po_syntezie:
        return "synteza"
    if not wynik.po_tescie_dzialania:
        return "test_dzialania"
    if not wynik.kandydaci:
        return "test_domkniecia"
    return None


def ocen_zgodnosc_domkniecia(model: dict, rekord: RekordDowodowy) -> dict[str, str]:
    """Porównuje jawnie nazwany mechanizm z literalnym wzorcem modelu.

    Funkcja działa tylko dla zapisu ``Wygasanie: ...`` albo
    ``Utrwalanie: ...``. Nie interpretuje swobodnej narracji domknięcia.
    """
    rodzaj = rekord.dane.get("warunek_domkniecia", ())
    surowe = rekord.domkniecie_surowe
    if len(rodzaj) != 1 or rodzaj[0] == "nieokreslony" or not surowe:
        return {}
    if ":" not in surowe:
        return {}
    mechanizm = _ascii(surowe.split(":", 1)[1].strip())
    wynik = {}
    for rodzina, definicja in model["rodziny"].items():
        wzorzec = _ascii(definicja["domkniecie"][rodzaj[0]])
        wynik[rodzina] = (
            "zgodne"
            if mechanizm in wzorzec or wzorzec in mechanizm
            else "sprzeczne"
        )
    return wynik
