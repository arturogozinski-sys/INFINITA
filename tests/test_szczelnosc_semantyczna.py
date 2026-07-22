# -*- coding: utf-8 -*-
import tempfile
import unittest
from pathlib import Path

from narzedzia.audyt_semantyczny import audit


def dokument(ident, typ, body="# T\n\n## Teza\nTreść kontrolna o odporności systemu i zachowaniu funkcji podczas zakłócenia.", refs=None, prod="kanon", epi="zweryfikowane"):
    refs = refs or []
    links = "\n".join(f"  - {x}" for x in refs)
    odw = f"\nodwolania:\n{links}" if refs else ""
    return f"""---
id: {ident}
typ: {typ}
tytul: Test {ident}
status_produkcyjny: {prod}
status_epistemiczny: {epi}
wersja: 1.0{odw}
---
{body}
"""


class TestSzczelnoscSemantyczna(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def zapisz(self, name, content):
        (self.root / name).write_text(content, encoding="utf-8")

    def test_konflikt_statusu_z_lokalizacja_blokuje(self):
        self.zapisz("M001.md", dokument("M001", "mechanizm", prod="kandydat"))
        errors, _ = audit(self.root)
        self.assertTrue(any("status_produkcyjny" in e for e in errors))

    def test_bledna_ranga_wzgledem_prefiksu_blokuje(self):
        self.zapisz("Z001.md", dokument("Z001", "mechanizm"))
        errors, _ = audit(self.root)
        self.assertTrue(any("nie zgadza się z prefiksem" in e for e in errors))

    def test_zmiana_nazwy_nie_ukrywa_duplikatu_id(self):
        self.zapisz("M001.md", dokument("M001", "mechanizm"))
        self.zapisz("inna_nazwa.md", dokument("M001", "mechanizm"))
        errors, _ = audit(self.root)
        self.assertTrue(any("zduplikowany identyfikator" in e for e in errors))

    def test_zerwana_relacja_jest_alarmem(self):
        self.zapisz("M001.md", dokument("M001", "mechanizm", refs=["Z999"]))
        errors, warnings = audit(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any("brak celu" in w for w in warnings))

    def test_osierocony_regulator_jest_alarmem(self):
        body = "# Z\n\n## Zasada\nZachowaj funkcję.\n\n## Granica\nNie oznacza bierności."
        self.zapisz("Z001.md", dokument("Z001", "zasada", body=body))
        _, warnings = audit(self.root)
        self.assertTrue(any("regulator bez odwołań" in w for w in warnings))

    def test_prawie_ten_sam_dokument_jest_sygnalizowany(self):
        body1 = "# A\n\n## Teza\nSystem zachowuje rezerwę czasu energii uwagi bezpieczeństwa korekty regeneracji odporności działania przyszłych opcji."
        body2 = "# B\n\n## Teza\nSystem zachowuje rezerwę czasu energii uwagi bezpieczeństwa korekty regeneracji odporności działania przyszłych opcji oraz margines."
        self.zapisz("M001.md", dokument("M001", "mechanizm", body=body1))
        self.zapisz("M002.md", dokument("M002", "mechanizm", body=body2))
        _, warnings = audit(self.root)
        self.assertTrue(any("możliwy dubel" in w for w in warnings))


if __name__ == "__main__":
    unittest.main(verbosity=2)
