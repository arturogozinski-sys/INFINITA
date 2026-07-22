# -*- coding: utf-8 -*-
"""P0.6 — raport martwych odwołań (00_FUNDAMENT/BRAKUJACE_ODWOLANIA.md).
Test adwersarialny: sztuczny kanon z celowo martwymi krawędziami (różna liczba
odwołań na cel, wiele źródeł) -> raport ma poprawnie zliczyć i wypisać źródła,
bez automatycznego "rozstrzygania" (żadnego importu, żadnej decyzji)."""
import importlib.util
import os, shutil, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rdzen.repozytorium import IndeksSQLite
from rdzen.parser import zbuduj_indeks

ROOT = os.path.join(os.path.dirname(__file__), '..')
SCHEMAT = os.path.join(ROOT, 'schemat_grafu.json')

MODUL_SCIEZKA = os.path.join(ROOT, 'narzedzia', 'generuj_raport_martwych_odwolan.py')
spec = importlib.util.spec_from_file_location('generuj_raport_martwych_odwolan', MODUL_SCIEZKA)
raport_modul = importlib.util.module_from_spec(spec)
spec.loader.exec_module(raport_modul)

A = """---
id: M910
typ: mechanizm
tytul: Ma dwa martwe odwolania
status_epistemiczny: zweryfikowane
wersja: 1.0
odwolania:
  - M800
  - M801
---
# M910
"""

B = """---
id: M911
typ: mechanizm
tytul: Odwoluje sie do tego samego martwego celu co M910
status_epistemiczny: zweryfikowane
wersja: 1.0
odwolania:
  - M800
---
# M911
"""


def _zbuduj_raport_dla(katalog):
    """Powiela logikę generuj_raport_martwych_odwolan.main(), ale na dowolnym katalogu
    (żeby nie dotykać prawdziwego kanon/ w teście)."""
    indeks = IndeksSQLite(':memory:')
    try:
        zbuduj_indeks(katalog, indeks, SCHEMAT)
        martwe = indeks.martwe_krawedzie()
    finally:
        indeks.close()
    from collections import defaultdict
    wg_cel = defaultdict(list)
    for m in martwe:
        wg_cel[m['cel']].append(m['zrodlo'])
    return wg_cel


class TestRaportMartwychOdwolan(unittest.TestCase):
    def test_liczenie_i_zrodla_poprawne_na_sztucznym_kanonie(self):
        tmp = tempfile.mkdtemp()
        try:
            with open(os.path.join(tmp, 'a.md'), 'w', encoding='utf-8') as f:
                f.write(A)
            with open(os.path.join(tmp, 'b.md'), 'w', encoding='utf-8') as f:
                f.write(B)

            wg_cel = _zbuduj_raport_dla(tmp)

            self.assertEqual(sorted(wg_cel['M800']), ['M910', 'M911'])
            self.assertEqual(len(wg_cel['M800']), 2)
            self.assertEqual(wg_cel['M801'], ['M910'])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_skrypt_produkcyjny_generuje_plik_z_tabela(self):
        """Regresja na prawdziwym kanon/: plik istnieje i ma nagłówki tabeli."""
        raport_modul.main()
        sciezka = raport_modul.WYJSCIE
        self.assertTrue(os.path.exists(sciezka))
        with open(sciezka, encoding='utf-8') as f:
            tresc = f.read()
        self.assertIn('| cel | ile odwołań | źródła |', tresc)
        self.assertIn('Razem martwych krawędzi', tresc)


if __name__ == '__main__':
    unittest.main(verbosity=2)
