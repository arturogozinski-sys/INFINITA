#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audyt produkcyjny: buduje indeks z PRAWDZIWEGO kanon/ (nie fikstury_demo/).
Używane przez CI (P0.2) — jeśli walidacja się nie powiedzie, proces kończy się
kodem 1 i wypisuje pełną listę naruszeń."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from rdzen.parser import zbuduj_indeks, BledyWalidacji
from rdzen.repozytorium import IndeksSQLite
from rdzen.walidator import Walidator

KANON = os.path.join(ROOT, 'kanon')
SCHEMAT = os.path.join(ROOT, 'schemat_grafu.json')


def main():
    indeks = IndeksSQLite(':memory:')
    try:
        n = zbuduj_indeks(KANON, indeks, SCHEMAT)
    except BledyWalidacji as e:
        print(f"Walidacja kanon/ NIE POWIODŁA SIĘ ({len(e.naruszenia)} naruszeń):")
        for naruszenie in e.naruszenia:
            print(f"  - {naruszenie}")
        return 1
    finally:
        indeks.close()

    wersja = Walidator(SCHEMAT).wersja_schematu
    print(f"Kanon zgodny ze schematem: {n} plików, wersja schematu {wersja}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
