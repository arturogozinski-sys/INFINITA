# -*- coding: utf-8 -*-
"""P0.1 — test adwersarialny transakcyjności zbuduj_indeks().
Dowód, że plik naruszający schemat przerywa CAŁĄ operację i nie zostawia
bazy w stanie częściowo zapisanym (parse_all -> validate_all -> validate_graph
-> transactional_replace, patrz rdzen/parser.py)."""
import os, sys, shutil, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rdzen.repozytorium import IndeksSQLite
from rdzen.parser import zbuduj_indeks, BledyWalidacji

SCHEMAT = os.path.join(os.path.dirname(__file__), '..', 'schemat_grafu.json')

GOOD_1 = """---
id: M900
typ: mechanizm
tytul: Test dobry 1
status_epistemiczny: zweryfikowane
wersja: 1.0
---
# M900
"""

GOOD_2 = """---
id: M901
typ: mechanizm
tytul: Test dobry 2
status_epistemiczny: zweryfikowane
wersja: 1.0
---
# M901
"""

BAD_TYP = """---
id: M902
typ: nieistniejacy_typ
tytul: Test zly
status_epistemiczny: zweryfikowane
wersja: 1.0
---
# M902
"""


class TestTransakcyjnoscBudowyIndeksu(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def _zapisz(self, nazwa, tresc):
        with open(os.path.join(self.tmp, nazwa), 'w', encoding='utf-8') as f:
            f.write(tresc)

    def test_zly_typ_przerywa_cala_operacje_baza_wraca_do_poprzedniego_stanu(self):
        indeks = IndeksSQLite(":memory:")
        self.addCleanup(indeks.close)

        # 1. ustal wcześniejszy, poprawny stan bazy (2 dobre pliki)
        self._zapisz('a.md', GOOD_1)
        self._zapisz('b.md', GOOD_2)
        zbuduj_indeks(self.tmp, indeks, SCHEMAT)
        przed = {w['id'] for w in indeks.wszystkie_wezly()}
        self.assertEqual(przed, {'M900', 'M901'})

        # 2. dopisz trzeci plik naruszający schemat (zły typ)
        self._zapisz('c.md', BAD_TYP)

        with self.assertRaises(BledyWalidacji) as ctx:
            zbuduj_indeks(self.tmp, indeks, SCHEMAT)

        # 3. błąd jest czytelny i wskazuje konkretne naruszenie
        self.assertTrue(any('nieznany typ' in n for n in ctx.exception.naruszenia),
                         ctx.exception.naruszenia)

        # 4. baza NIE została dotknięta — pozostaje w poprzednim stanie
        po = {w['id'] for w in indeks.wszystkie_wezly()}
        self.assertEqual(po, przed)
        self.assertNotIn('M902', po)

    def test_zla_probka_od_zera_zostawia_baze_pusta(self):
        self._zapisz('a.md', GOOD_1)
        self._zapisz('b.md', BAD_TYP)

        indeks = IndeksSQLite(":memory:")
        self.addCleanup(indeks.close)
        indeks.rebuild()  # stan początkowy: pusta, zainicjalizowana baza

        with self.assertRaises(BledyWalidacji):
            zbuduj_indeks(self.tmp, indeks, SCHEMAT)

        self.assertEqual(indeks.wszystkie_wezly(), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
