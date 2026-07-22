# -*- coding: utf-8 -*-
"""Test end-to-end: plik kanonu -> parser -> indeks -> zapytanie.
Dowód, że element przechodzi całą drogę i że graf + czujnik integralności działają."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rdzen.repozytorium import IndeksSQLite
from rdzen.parser import zbuduj_indeks
from rdzen.walidator import Walidator

KANON = os.path.join(os.path.dirname(__file__), '..', 'fikstury_demo')
SCHEMAT = os.path.join(os.path.dirname(__file__), '..', 'schemat_grafu.json')

def main():
    indeks = IndeksSQLite(":memory:")   # silnik wymienny; tu SQLite w pamięci
    n = zbuduj_indeks(KANON, indeks)
    schema_version = Walidator(SCHEMAT).wersja_schematu
    print(f"Zbudowano indeks z {n} plików wejściowych (fikstury demonstracyjne, schema {schema_version})")

    # 1. węzeł przeszedł całą drogę
    w = indeks.wezel('M045')
    assert w is not None, "M045 nie dotarł do indeksu"
    print(f"\nWęzeł M045: typ={w['typ']}, tytuł='{w['tytul']}', status={w['status_epistemiczny']}, źródła={w['zrodla']}")

    # 2. krawędzie zbudowane
    kraw = indeks.krawedzie_z('M045')
    print(f"Krawędzie z M045: {[(k['cel'], k['typ']) for k in kraw]}")
    assert any(k['cel'] == 'M044' for k in kraw), "brak krawędzi M045->M044"

    # 3. czujnik integralności: martwy link M044->M999 (M999 nie istnieje)
    martwe = indeks.martwe_krawedzie()
    print(f"\nCzujnik martwych krawędzi: {[(m['zrodlo'], m['cel']) for m in martwe]}")
    assert any(m['cel'] == 'M999' for m in martwe), "czujnik nie wykrył martwego linku"
    assert not any(m['cel'] == 'M044' for m in martwe), "M044 istnieje, nie powinien być martwy"

    # 4. odtwarzalność: przebuduj od zera, wynik identyczny
    przed = len(indeks.wszystkie_wezly())
    zbuduj_indeks(KANON, indeks)
    po = len(indeks.wszystkie_wezly())
    assert przed == po, "przebudowa zmieniła liczbę węzłów"
    print(f"\nOdtwarzalność: przebudowa z plików -> {po} węzłów (identycznie)")

    indeks.close()
    print("\n=== WSZYSTKO OK: plik -> parser -> indeks -> zapytanie -> czujnik ===")

if __name__ == '__main__':
    main()
