# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from narzedzia.audyt_semantyczny import audit, ids_from_declared_links


class TestAudytSemantyczny(unittest.TestCase):
    def test_biezacy_kanon_nie_ma_bledow_semantycznych_twardych(self):
        errors, _warnings = audit()
        self.assertEqual(errors, [])

    def test_czujnik_odczytuje_jawne_powiazania_z_tresci(self):
        body = "Powiązania kanoniczne: M018, Z006, S016.\n"
        self.assertEqual(ids_from_declared_links(body), {'M018', 'Z006', 'S016'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
