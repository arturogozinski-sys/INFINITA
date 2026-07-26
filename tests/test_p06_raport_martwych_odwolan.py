# -*- coding: utf-8 -*-
"""Raport martwych odwołań nie może modyfikować śledzonych plików w teście."""
import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from narzedzia.generuj_raport_martwych_odwolan import (  # noqa: E402
    main,
    renderuj,
    zbierz_martwe_odwolania,
)

SCHEMAT = ROOT / "schemat_grafu.json"

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


class TestRaportMartwychOdwolan(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.kanon = self.root / "kanon"
        self.kanon.mkdir()
        (self.kanon / "a.md").write_text(A, encoding="utf-8", newline="\n")
        (self.kanon / "b.md").write_text(B, encoding="utf-8", newline="\n")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_liczenie_i_zrodla_poprawne(self):
        wg_cel = zbierz_martwe_odwolania(self.kanon, SCHEMAT)
        self.assertEqual(wg_cel["M800"], ["M910", "M911"])
        self.assertEqual(wg_cel["M801"], ["M910"])

    def test_skrypt_zapisuje_wylacznie_wskazane_wyjscie(self):
        output = self.root / "raport.md"
        registry = self.root / "registry.json"
        registry.write_text(
            json.dumps(
                {
                    "wpisy": {
                        "M800": {
                            "klasa": "planowany",
                            "termin": "2099-01-01",
                        },
                        "M801": {
                            "klasa": "zewnetrzny",
                            "termin": "2099-01-01",
                        },
                    }
                }
            ),
            encoding="utf-8",
        )
        tracked_report = ROOT / "00_FUNDAMENT" / "BRAKUJACE_ODWOLANIA.md"
        before = tracked_report.read_bytes()

        result = main(
            [
                "--kanon",
                str(self.kanon),
                "--schemat",
                str(SCHEMAT),
                "--rejestr",
                str(registry),
                "--output",
                str(output),
                "--today",
                "2026-07-26",
            ]
        )

        self.assertEqual(result, 0)
        self.assertEqual(tracked_report.read_bytes(), before)
        self.assertIn("| M800 | 2 | M910, M911 |", output.read_text(encoding="utf-8"))

    def test_przeterminowany_wpis_staje_sie_blokerem(self):
        tekst, blokery = renderuj(
            {"M800": ["M910"]},
            {"wpisy": {"M800": {"klasa": "planowany", "termin": "2026-07-25"}}},
            dt.date(2026, 7, 26),
        )
        self.assertIn("BLOCKER: termin minął", tekst)
        self.assertEqual(len(blokery), 1)

    def test_klasa_blad_blokuje_od_razu(self):
        _, blokery = renderuj(
            {"M800": ["M910"]},
            {"wpisy": {"M800": {"klasa": "blad", "termin": "2026-07-26"}}},
            dt.date(2026, 7, 26),
        )
        self.assertEqual(len(blokery), 1)

    def test_nowy_cel_bez_wpisu_w_rejestrze_blokuje(self):
        _, blokery = renderuj(
            {"M802": ["M910"]},
            {"wpisy": {}},
            dt.date(2026, 7, 26),
        )
        self.assertEqual(len(blokery), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
