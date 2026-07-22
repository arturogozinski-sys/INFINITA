# -*- coding: utf-8 -*-
"""P0.2 — CI ma audytować PRAWDZIWY kanon/, nie fikstury_demo/.
Dwa testy: (1) regresja — obecny kanon/ musi przechodzić przez narzędzie CI;
(2) adwersarialny — plik naruszający schemat wstawiony do kopii kanon/ musi
zawalić skrypt użyty w workflow (kod wyjścia 1, czytelny komunikat)."""
import os, sys, shutil, subprocess, tempfile, unittest

ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, ROOT)
from rdzen.parser import zbuduj_indeks
from rdzen.repozytorium import IndeksSQLite

KANON = os.path.join(ROOT, 'kanon')
SCHEMAT = os.path.join(ROOT, 'schemat_grafu.json')
SKRYPT_CI = os.path.join(ROOT, 'narzedzia', 'zbuduj_kanon.py')

BAD_TYP = """---
id: M998
typ: nieistniejacy_typ
tytul: Test zly do audytu CI
status_epistemiczny: zweryfikowane
wersja: 1.0
---
# M998
"""


class TestAudytKanonuWCI(unittest.TestCase):
    def test_prawdziwy_kanon_przechodzi_walidacje(self):
        """Regresja: obecny stan kanon/ musi być zgodny ze schematem (to jest audyt CI)."""
        indeks = IndeksSQLite(':memory:')
        self.addCleanup(indeks.close)
        n = zbuduj_indeks(KANON, indeks, SCHEMAT)
        self.assertGreater(n, 0)

    def test_skrypt_ci_failuje_na_uszkodzonym_kanonie(self):
        """Adwersarialny: kopia kanon/ + plik z błędnym typem -> skrypt CI ma zwrócić kod 1."""
        tmp = tempfile.mkdtemp()
        try:
            tmp_kanon = os.path.join(tmp, 'kanon')
            shutil.copytree(KANON, tmp_kanon)
            with open(os.path.join(tmp_kanon, 'zly.md'), 'w', encoding='utf-8') as f:
                f.write(BAD_TYP)
            shutil.copy(SCHEMAT, os.path.join(tmp, 'schemat_grafu.json'))
            shutil.copytree(os.path.join(ROOT, 'rdzen'), os.path.join(tmp, 'rdzen'))
            shutil.copytree(os.path.join(ROOT, 'narzedzia'), os.path.join(tmp, 'narzedzia'))

            env = dict(os.environ, PYTHONIOENCODING='utf-8')
            wynik = subprocess.run(
                [sys.executable, os.path.join(tmp, 'narzedzia', 'zbuduj_kanon.py')],
                cwd=tmp, capture_output=True, text=True, encoding='utf-8', timeout=30, env=env,
            )
            self.assertEqual(wynik.returncode, 1, wynik.stdout + wynik.stderr)
            self.assertIn('nieznany typ', wynik.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
