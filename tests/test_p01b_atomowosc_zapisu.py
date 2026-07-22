# -*- coding: utf-8 -*-
"""Test adwersarialny: błąd W TRAKCIE zapisu cofa całą wymianę indeksu."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rdzen.repozytorium import IndeksSQLite


class TestAtomowoscZapisuSQLite(unittest.TestCase):
    def setUp(self):
        self.indeks = IndeksSQLite(':memory:')
        self.addCleanup(self.indeks.close)

        stary = {
            'id': 'M900',
            'typ': 'mechanizm',
            'tytul': 'Poprzedni poprawny stan',
            'status_epistemiczny': 'zweryfikowane',
            'wersja': '1.0',
            'zrodla': [],
            'sciezka': 'stary.md',
        }
        self.indeks.zamien_wszystko_atomowo([stary], [], '1.0')

    def test_blad_serializacji_po_pierwszym_insercie_przywraca_stary_indeks(self):
        dobry_nowy = {
            'id': 'M901',
            'typ': 'mechanizm',
            'tytul': 'Pierwszy nowy węzeł',
            'status_epistemiczny': 'zweryfikowane',
            'wersja': '1.0',
            'zrodla': [],
            'sciezka': 'nowy_1.md',
        }
        wadliwy_nowy = {
            'id': 'M902',
            'typ': 'mechanizm',
            'tytul': 'Błąd podczas serializacji',
            'status_epistemiczny': 'zweryfikowane',
            'wersja': '1.0',
            # set nie jest serializowalny do JSON. Błąd wystąpi po utworzeniu
            # nowych tabel i po zapisaniu M901, czyli naprawdę w połowie operacji.
            'zrodla': {'E001'},
            'sciezka': 'nowy_2.md',
        }

        with self.assertRaises(TypeError):
            self.indeks.zamien_wszystko_atomowo(
                [dobry_nowy, wadliwy_nowy],
                [],
                '2.0',
            )

        # Cała nieudana wymiana została cofnięta: stary węzeł nadal istnieje,
        # żaden nowy nie przeciekł do bazy, a wersja schematu też pozostała stara.
        self.assertEqual(
            {w['id'] for w in self.indeks.wszystkie_wezly()},
            {'M900'},
        )
        self.assertIsNone(self.indeks.wezel('M901'))
        self.assertIsNone(self.indeks.wezel('M902'))
        wersja = self.indeks.db.execute(
            "SELECT wartosc FROM meta WHERE klucz='schema_version'"
        ).fetchone()
        self.assertEqual(wersja['wartosc'], '1.0')


if __name__ == '__main__':
    unittest.main(verbosity=2)
