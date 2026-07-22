# -*- coding: utf-8 -*-
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rdzen.repozytorium import IndeksSQLite, SCHEMA_VERSION
from rdzen.parser import zbuduj_indeks

FIKSTURY = os.path.join(os.path.dirname(__file__), '..', 'fikstury_demo')

class TestPrzeplywEndToEnd(unittest.TestCase):
    def setUp(self):
        self.indeks = IndeksSQLite(":memory:")
        self.addCleanup(self.indeks.close)
        self.n = zbuduj_indeks(FIKSTURY, self.indeks)

    def test_wezel_przeszedl_cala_droge(self):
        w = self.indeks.wezel('M045')
        self.assertIsNotNone(w)
        self.assertEqual(w['typ'], 'mechanizm')
        self.assertEqual(w['status_epistemiczny'], 'demonstracyjne')

    def test_krawedzie_powstaly(self):
        cele = {k['cel'] for k in self.indeks.krawedzie_z('M045')}
        self.assertIn('M044', cele)

    def test_czujnik_martwych_krawedzi(self):
        martwe = {m['cel'] for m in self.indeks.martwe_krawedzie()}
        self.assertIn('M999', martwe)
        self.assertNotIn('M044', martwe)

    def test_odtwarzalnosc_indeksu(self):
        przed = len(self.indeks.wszystkie_wezly())
        zbuduj_indeks(FIKSTURY, self.indeks)
        self.assertEqual(przed, len(self.indeks.wszystkie_wezly()))

    def test_wersja_schematu_zapisana(self):
        r = self.indeks.db.execute("SELECT wartosc FROM meta WHERE klucz='schema_version'").fetchone()
        self.assertEqual(r['wartosc'], SCHEMA_VERSION)

if __name__ == '__main__':
    unittest.main(verbosity=2)
