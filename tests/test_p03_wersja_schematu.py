# -*- coding: utf-8 -*-
"""P0.3 — wersja schematu ma jedno źródło: pole "wersja" w schemat_grafu.json.
Test adwersarialny: podmieniamy wersję w kopii JSON na wartość, która nigdzie
w kodzie nie występuje, i sprawdzamy że meta.schema_version przyjmuje DOKŁADNIE
tę wartość. To nie jest porównanie stałej do samej siebie — JSON jest jedynym
źródłem odczytu w teście."""
import json, os, shutil, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rdzen.repozytorium import IndeksSQLite
from rdzen.parser import zbuduj_indeks

ROOT = os.path.join(os.path.dirname(__file__), '..')
SCHEMAT_ORYG = os.path.join(ROOT, 'schemat_grafu.json')
FIKSTURY = os.path.join(ROOT, 'fikstury_demo')

WERSJA_TESTOWA = "9.9-test-p03-nie-uzywana-nigdzie-indziej"


class TestWersjaSchematuZJednegoZrodla(unittest.TestCase):
    def test_wersja_w_meta_pochodzi_realnie_z_json(self):
        with open(SCHEMAT_ORYG, encoding='utf-8') as f:
            dane = json.load(f)
        self.assertNotEqual(dane['wersja'], WERSJA_TESTOWA,
                             "wartość testowa musi się realnie różnić od aktualnej")
        dane['wersja'] = WERSJA_TESTOWA

        tmp = tempfile.mkdtemp()
        try:
            sciezka_testowa = os.path.join(tmp, 'schemat_grafu.json')
            with open(sciezka_testowa, 'w', encoding='utf-8') as f:
                json.dump(dane, f, ensure_ascii=False)

            indeks = IndeksSQLite(":memory:")
            try:
                zbuduj_indeks(FIKSTURY, indeks, sciezka_testowa)
                r = indeks.db.execute(
                    "SELECT wartosc FROM meta WHERE klucz='schema_version'").fetchone()
                self.assertEqual(r['wartosc'], WERSJA_TESTOWA)
            finally:
                indeks.close()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_brak_hardcoded_stalej_w_repozytorium(self):
        import rdzen.repozytorium as repo
        self.assertFalse(hasattr(repo, 'SCHEMA_VERSION'),
                          "SCHEMA_VERSION nie powinno już istnieć jako stała w kodzie")


if __name__ == '__main__':
    unittest.main(verbosity=2)
