#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P0.6 — generuje 00_FUNDAMENT/BRAKUJACE_ODWOLANIA.md: listę martwych krawędzi
w kanon/ (odwołania do identyfikatorów, których nie ma w kanonie).
To jest materiał do decyzji właściciela — skrypt NIE decyduje, czy cel jest
jeszcze niezaimportowany, archiwalny, zewnętrzny czy błędny."""
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from rdzen.parser import zbuduj_indeks
from rdzen.repozytorium import IndeksSQLite

KANON = os.path.join(ROOT, 'kanon')
SCHEMAT = os.path.join(ROOT, 'schemat_grafu.json')
WYJSCIE = os.path.join(ROOT, '00_FUNDAMENT', 'BRAKUJACE_ODWOLANIA.md')


def main():
    indeks = IndeksSQLite(':memory:')
    try:
        zbuduj_indeks(KANON, indeks, SCHEMAT)
        martwe = indeks.martwe_krawedzie()
    finally:
        indeks.close()

    wg_cel = defaultdict(list)
    for m in martwe:
        wg_cel[m['cel']].append(m['zrodlo'])

    linie = [
        "# Brakujące odwołania (martwe krawędzie w kanon/)",
        "",
        "Wygenerowane automatycznie przez `narzedzia/generuj_raport_martwych_odwolan.py`. "
        "Nie jest to lista do automatycznego importu — decyzja co zrobić z każdym celem "
        "(jeszcze niezaimportowane / archiwalne / zewnętrzne / błędne odwołanie) należy "
        "do właściciela.",
        "",
        f"Razem martwych krawędzi: **{len(martwe)}**, unikalnych celów: **{len(wg_cel)}**.",
        "",
        "| cel | ile odwołań | źródła |",
        "|---|---|---|",
    ]
    for cel, zrodla in sorted(wg_cel.items()):
        zrodla_sorted = sorted(zrodla)
        linie.append(f"| {cel} | {len(zrodla_sorted)} | {', '.join(zrodla_sorted)} |")
    linie.append("")

    os.makedirs(os.path.dirname(WYJSCIE), exist_ok=True)
    with open(WYJSCIE, 'w', encoding='utf-8') as f:
        f.write("\n".join(linie))

    print(f"Zapisano {WYJSCIE} ({len(wg_cel)} celów, {len(martwe)} martwych krawędzi)")


if __name__ == '__main__':
    main()
