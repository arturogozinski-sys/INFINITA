# -*- coding: utf-8 -*-
"""P0.4 — duplikat ID musi być błędem, nie cichym nadpisaniem.
Test adwersarialny: dwa pliki z tym samym id M100 -> cała operacja ma polec
(BledyWalidacji z validate_graph), baza nie zawiera żadnego z nich."""
import os, sys, shutil, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rdzen.repozytorium import IndeksSQLite
from rdzen.parser import zbuduj_indeks, BledyWalidacji

SCHEMAT = os.path.join(os.path.dirname(__file__), '..', 'schemat_grafu.json')

M100_WERSJA_A = """---
id: M100
typ: mechanizm
tytul: Wersja A tego samego id
status_epistemiczny: zweryfikowane
wersja: 1.0
---
# M100 wersja A
"""

M100_WERSJA_B = """---
id: M100
typ: mechanizm
tytul: Wersja B tego samego id
status_epistemiczny: zweryfikowane
wersja: 1.0
---
# M100 wersja B
"""


class TestDuplikatIdJestBledem(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def _zapisz(self, nazwa, tresc):
        with open(os.path.join(self.tmp, nazwa), 'w', encoding='utf-8') as f:
            f.write(tresc)

    def test_duplikat_id_w_dwoch_plikach_przerywa_operacje(self):
        self._zapisz('a.md', M100_WERSJA_A)
        self._zapisz('b.md', M100_WERSJA_B)

        indeks = IndeksSQLite(":memory:")
        self.addCleanup(indeks.close)
        indeks.rebuild()  # pusty stan początkowy

        with self.assertRaises(BledyWalidacji) as ctx:
            zbuduj_indeks(self.tmp, indeks, SCHEMAT)

        naruszenia = ctx.exception.naruszenia
        self.assertTrue(any('zduplikowany identyfikator' in n and 'M100' in n for n in naruszenia),
                         naruszenia)
        # błąd wskazuje OBA pliki
        komunikat = ' '.join(naruszenia)
        self.assertIn('a.md', komunikat)
        self.assertIn('b.md', komunikat)

        # baza nie zawiera żadnego z nich
        self.assertIsNone(indeks.wezel('M100'))
        self.assertEqual(indeks.wszystkie_wezly(), [])

    def test_dodaj_wezel_odrzuca_duplikat_na_poziomie_bazy(self):
        """Druga linia obrony: gdyby ktoś ominął validate_graph, baza sama odmawia."""
        import sqlite3
        indeks = IndeksSQLite(":memory:")
        self.addCleanup(indeks.close)
        indeks.rebuild()
        wezel = {'id': 'M100', 'typ': 'mechanizm', 'tytul': 'X',
                  'status_epistemiczny': 'zweryfikowane', 'wersja': '1.0'}
        indeks.dodaj_wezel(wezel)
        with self.assertRaises(sqlite3.IntegrityError):
            indeks.dodaj_wezel(wezel)


if __name__ == '__main__':
    unittest.main(verbosity=2)
