# -*- coding: utf-8 -*-
"""P0.5 — narzedzia/audyt.py usunięty (szukał nieistniejącego już pola "status";
dublował rolę Walidator z rdzen/walidator.py, ale gorzej).
Dowód, że usunięcie nie zostawia dziury: plik bez nagłówka YAML w kanon-podobnym
katalogu — dokładnie to, co audyt.py kiedyś łapał jako 'brak nagłówka YAML' —
nadal zostaje wykryty, tyle że przez zbuduj_indeks()/Walidator."""
import os, shutil, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rdzen.repozytorium import IndeksSQLite
from rdzen.parser import zbuduj_indeks, BledyWalidacji

ROOT = os.path.join(os.path.dirname(__file__), '..')
SCHEMAT = os.path.join(ROOT, 'schemat_grafu.json')

BRAK_NAGLOWKA_YAML = "# Dokument bez nagłówka YAML\nTreść bez front-matter.\n"


class TestAudytUsuniety(unittest.TestCase):
    def test_narzedzie_audyt_py_nie_istnieje(self):
        self.assertFalse(os.path.exists(os.path.join(ROOT, 'narzedzia', 'audyt.py')))

    def test_walidator_wykrywa_brak_naglowka_yaml_zamiast_audyt_py(self):
        tmp = tempfile.mkdtemp()
        try:
            with open(os.path.join(tmp, 'bez_naglowka.md'), 'w', encoding='utf-8') as f:
                f.write(BRAK_NAGLOWKA_YAML)

            indeks = IndeksSQLite(":memory:")
            self.addCleanup(indeks.close)
            indeks.rebuild()

            with self.assertRaises(BledyWalidacji) as ctx:
                zbuduj_indeks(tmp, indeks, SCHEMAT)

            self.assertTrue(any('nieznany typ' in n for n in ctx.exception.naruszenia),
                             ctx.exception.naruszenia)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
