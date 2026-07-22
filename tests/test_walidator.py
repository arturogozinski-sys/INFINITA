# -*- coding: utf-8 -*-
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rdzen.walidator import Walidator

SCHEMAT = os.path.join(os.path.dirname(__file__), '..', 'schemat_grafu.json')

class TestWalidator(unittest.TestCase):
    def setUp(self):
        self.w = Walidator(SCHEMAT)

    def test_poprawny_wezel_przechodzi(self):
        wezel = {'id': 'M045', 'typ': 'mechanizm', 'tytul': 'X', 'status_epistemiczny': 'zweryfikowane', 'wersja': '0.1'}
        self.assertEqual(self.w.sprawdz_wezel(wezel), [])

    def test_nieznany_typ_lapany(self):
        wezel = {'id': 'M045', 'typ': 'wymyslony_typ', 'tytul': 'X', 'status_epistemiczny': 'zweryfikowane', 'wersja': '0.1'}
        self.assertTrue(any('nieznany typ' in n for n in self.w.sprawdz_wezel(wezel)))

    def test_prefiks_niezgodny_z_typem_lapany(self):
        wezel = {'id': 'E045', 'typ': 'mechanizm', 'tytul': 'X', 'status_epistemiczny': 'zweryfikowane', 'wersja': '0.1'}
        self.assertTrue(any('nie odpowiada typowi' in n for n in self.w.sprawdz_wezel(wezel)))

    def test_brak_pola_wymaganego_lapany(self):
        wezel = {'id': 'M045', 'typ': 'mechanizm', 'tytul': 'X', 'status_epistemiczny': 'zweryfikowane'}
        self.assertTrue(any("brak wymaganego pola 'wersja'" in n for n in self.w.sprawdz_wezel(wezel)))

    def test_zly_status_epistemiczny_lapany(self):
        wezel = {'id': 'M045', 'typ': 'mechanizm', 'tytul': 'X', 'status_epistemiczny': 'wymyslony', 'wersja': '0.1'}
        self.assertTrue(any('niedozwolony status_epistemiczny' in n for n in self.w.sprawdz_wezel(wezel)))

    def test_id_niezgodny_z_wzorcem_lapany(self):
        wezel = {'id': 'mechanizm-45', 'typ': 'mechanizm', 'tytul': 'X', 'status_epistemiczny': 'zweryfikowane', 'wersja': '0.1'}
        self.assertTrue(any('niezgodny z wzorcem' in n for n in self.w.sprawdz_wezel(wezel)))

    def test_wiarygodnosc_dowodu_poza_zakresem_lapana(self):
        wezel = {'id': 'E003', 'typ': 'dowod', 'tytul': 'X', 'status_epistemiczny': 'zweryfikowane', 'wiarygodnosc': 9}
        self.assertTrue(any("poza zakresem 1-5" in n for n in self.w.sprawdz_wezel(wezel)))

    def test_poprawny_dowod_przechodzi(self):
        wezel = {'id': 'E003', 'typ': 'dowod', 'tytul': 'X', 'status_epistemiczny': 'zweryfikowane', 'wiarygodnosc': 4}
        self.assertEqual(self.w.sprawdz_wezel(wezel), [])

if __name__ == '__main__':
    unittest.main(verbosity=2)
