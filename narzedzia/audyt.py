#!/usr/bin/env python3
"""Audyt plików .md w kanon/ i robocze/."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KATALOGI = ["kanon", "robocze"]
WZORZEC_WERSJI = re.compile(r"^(?P<baza>.+)_v(?P<wersja>\d+(?:\.\d+)*)\.md$")


def ma_naglowek_yaml(tresc):
    return tresc.startswith("---")


def blok_yaml(tresc):
    if not ma_naglowek_yaml(tresc):
        return None
    linie = tresc.split("\n")
    for i in range(1, len(linie)):
        if linie[i].strip() == "---":
            return "\n".join(linie[1:i])
    return None


def ma_pole_status(tresc):
    blok = blok_yaml(tresc)
    if blok is None:
        return False
    return re.search(r"^status\s*:", blok, re.MULTILINE) is not None


def zbierz_pliki_md():
    pliki = []
    for katalog in KATALOGI:
        sciezka = ROOT / katalog
        if not sciezka.is_dir():
            continue
        for plik in sorted(sciezka.rglob("*.md")):
            pliki.append(plik)
    return pliki


def audytuj():
    problemy = []
    pliki = zbierz_pliki_md()

    wersje_wg_bazy = {}

    for plik in pliki:
        wzgledna = plik.relative_to(ROOT).as_posix()
        try:
            tresc = plik.read_text(encoding="utf-8")
        except Exception as e:
            problemy.append(f"{wzgledna}: nie można odczytać pliku ({e})")
            continue

        if len(tresc.strip()) < 100:
            problemy.append(f"{wzgledna}: plik pusty lub krótszy niż 100 znaków")

        if not ma_naglowek_yaml(tresc):
            problemy.append(f"{wzgledna}: brak nagłówka YAML (--- na początku)")
        elif plik.parent.name == "kanon" and not ma_pole_status(tresc):
            problemy.append(f"{wzgledna}: brak pola status")

        if plik.parent.name == "kanon" and ma_naglowek_yaml(tresc) and blok_yaml(tresc) is None:
            problemy.append(f"{wzgledna}: niezamknięty nagłówek YAML")

        dopasowanie = WZORZEC_WERSJI.match(plik.name)
        if dopasowanie:
            baza = dopasowanie.group("baza")
            wersje_wg_bazy.setdefault(baza, []).append(wzgledna)

    for baza, wystapienia in sorted(wersje_wg_bazy.items()):
        if len(wystapienia) > 1:
            lista = ", ".join(sorted(wystapienia))
            problemy.append(f"{baza}: wiele wersji tego samego pliku ({lista})")

    return problemy


def main():
    problemy = audytuj()
    if not problemy:
        print("czysto")
        return 0
    for problem in problemy:
        print(problem)
    return 1


if __name__ == "__main__":
    sys.exit(main())
