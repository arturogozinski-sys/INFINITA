# -*- coding: utf-8 -*-
"""Formalny test wykrywalny przez pytest i unittest (dług techniczny nr 1).
Uruchomienie: pytest  albo  python -m unittest
CI (GitHub Actions) wykryje go automatycznie."""
import json, os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rdzen.repozytorium import IndeksSQLite
from rdzen.parser import zbuduj_indeks

FIKSTURY = os.path.join(os.path.dirname(__file__), '..', 'fikstury_demo')
SCHEMAT = os.path.join(os.path.dirname(__file__), '..', 'schemat_grafu.json')

class TestPrzeplywEndToEnd(unittest.TestCase):
    def setUp(self):
        self.indeks = IndeksSQLite(":memory:")
        self.addCleanup(self.indeks.close)
        self.n = zbuduj_indeks(FIKSTURY, self.indeks)

    def test_wezel_przeszedl_cala_droge(self):
        w = self.indeks.wezel('M045')
        self.assertIsNotNone(w)
        self.assertEqual(w['typ'], 'mechanizm')
        self.assertEqual(w['status_epistemiczny'], 'demonstracyjne')  # NIE kanon

    def test_krawedzie_powstaly(self):
        cele = {k['cel'] for k in self.indeks.krawedzie_z('M045')}
        self.assertIn('M044', cele)

    def test_czujnik_martwych_krawedzi(self):
        martwe = {m['cel'] for m in self.indeks.martwe_krawedzie()}
        self.assertIn('M999', martwe)          # nieistniejący -> wykryty
        self.assertNotIn('M044', martwe)       # istniejący -> nie martwy

    def test_odtwarzalnosc_indeksu(self):
        przed = len(self.indeks.wszystkie_wezly())
        zbuduj_indeks(FIKSTURY, self.indeks)
        self.assertEqual(przed, len(self.indeks.wszystkie_wezly()))

    def test_wersja_schematu_zapisana(self):
        # jedyne źródło prawdy to plik JSON — czytamy go niezależnie, bez importu stałej z kodu
        with open(SCHEMAT, encoding='utf-8') as f:
            wersja_z_pliku = json.load(f)['wersja']
        r = self.indeks.db.execute("SELECT wartosc FROM meta WHERE klucz='schema_version'").fetchone()
        self.assertEqual(r['wartosc'], wersja_z_pliku)

if __name__ == '__main__':
    unittest.main(verbosity=2)
