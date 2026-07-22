# -*- coding: utf-8 -*-
"""Test end-to-end: plik kanonu -> parser -> indeks -> zapytanie."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rdzen.repozytorium import IndeksSQLite, SCHEMA_VERSION
from rdzen.parser import zbuduj_indeks

KANON = os.path.join(os.path.dirname(__file__), '..', 'fikstury_demo')

def main():
    indeks = IndeksSQLite(":memory:")
    n = zbuduj_indeks(KANON, indeks)
    print(f"Zbudowano indeks z {n} plików wejściowych (fikstury demonstracyjne, schema {SCHEMA_VERSION})")
    w = indeks.wezel('M045')
    assert w is not None, "M045 nie dotarł do indeksu"
    print(f"\nWęzeł M045: typ={w['typ']}, tytuł='{w['tytul']}', status={w['status_epistemiczny']}, źródła={w['zrodla']}")
    kraw = indeks.krawedzie_z('M045')
    print(f"Krawędzie z M045: {[(k['cel'], k['typ']) for k in kraw]}")
    assert any(k['cel'] == 'M044' for k in kraw), "brak krawędzi M045->M044"
    martwe = indeks.martwe_krawedzie()
    print(f"\nCzujnik martwych krawędzi: {[(m['zrodlo'], m['cel']) for m in martwe]}")
    assert any(m['cel'] == 'M999' for m in martwe), "czujnik nie wykrył martwego linku"
    assert not any(m['cel'] == 'M044' for m in martwe), "M044 istnieje, nie powinien być martwy"
    przed = len(indeks.wszystkie_wezly())
    zbuduj_indeks(KANON, indeks)
    po = len(indeks.wszystkie_wezly())
    assert przed == po, "przebudowa zmieniła liczbę węzłów"
    print(f"\nOdtwarzalność: przebudowa z plików -> {po} węzłów (identycznie)")
    indeks.close()
    print("\n=== WSZYSTKO OK: plik -> parser -> indeks -> zapytanie -> czujnik ===")

if __name__ == '__main__':
    main()
