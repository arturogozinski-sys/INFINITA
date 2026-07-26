import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from narzedzia.waliduj_handoff import parse_simple_yaml, validate  # noqa: E402


class TestHandoff(unittest.TestCase):
    def test_szablon_ma_pelna_strukture(self):
        text = (ROOT / "przekazania" / "HANDOFF_TEMPLATE.yaml").read_text(
            encoding="utf-8"
        )
        self.assertEqual(validate(parse_simple_yaml(text), template=True), [])

    def test_poprawne_przekazanie_przechodzi(self):
        text = (ROOT / "przekazania" / "HANDOFF_TEMPLATE.yaml").read_text(
            encoding="utf-8"
        )
        text = (
            text.replace("UZUPELNIJ_PELNY_SHA", "a" * 40)
            .replace('"claude|copilot|gpt|czlowiek"', '"gpt"')
            .replace('"YYYY-MM-DD"', '"2026-07-26"')
            .replace(
                '"implementacja|audyt|symulacja|synteza|redakcja|diagnoza"',
                '"implementacja"',
            )
            .replace('id: "UZUPELNIJ"', 'id: "T001"')
            .replace('"snapshot|patch|raport"', '"patch"')
            .replace('katalog_lub_plik: "UZUPELNIJ"', 'katalog_lub_plik: "wynik.patch"')
            .replace("testy_oczekiwane: null", "testy_oczekiwane: 50")
            .replace(
                '"nieuruchomione|sukces|blad|czesciowy"',
                '"sukces"',
            )
            .replace("drzewo_czyste_po_testach: null", "drzewo_czyste_po_testach: true")
        )
        self.assertEqual(validate(parse_simple_yaml(text)), [])

    def test_sukces_bez_czystego_drzewa_jest_odrzucany(self):
        template = (ROOT / "przekazania" / "HANDOFF_TEMPLATE.yaml").read_text(
            encoding="utf-8"
        )
        parsed = parse_simple_yaml(template)
        parsed["commit_bazowy"] = "b" * 40
        parsed["wykonawca"] = "gpt"
        parsed["data_utworzenia"] = "2026-07-26"
        parsed["tryb"] = "audyt"
        parsed["zadanie.id"] = "T002"
        parsed["wynik.typ"] = "raport"
        parsed["wynik.katalog_lub_plik"] = "raport.md"
        parsed["walidacja.testy_oczekiwane"] = 50
        parsed["walidacja.wynik_deklarowany"] = "sukces"
        parsed["walidacja.drzewo_czyste_po_testach"] = False
        errors = validate(parsed)
        self.assertTrue(any("drzewo_czyste" in error for error in errors))

    def test_placeholder_enum_i_wyjscie_poza_repo_sa_odrzucane(self):
        template = (ROOT / "przekazania" / "HANDOFF_TEMPLATE.yaml").read_text(
            encoding="utf-8"
        )
        parsed = parse_simple_yaml(template)
        parsed["commit_bazowy"] = "c" * 40
        parsed["wykonawca"] = "dowolny"
        parsed["data_utworzenia"] = "2026-07-26"
        parsed["tryb"] = "audyt"
        parsed["zadanie.id"] = "T003"
        parsed["wynik.typ"] = "raport"
        parsed["wynik.katalog_lub_plik"] = "../raport.md"
        parsed["walidacja.wynik_deklarowany"] = "nieuruchomione"
        errors = validate(parsed)
        self.assertTrue(any("wykonawca" in error for error in errors))
        self.assertTrue(any("nie może zawierać .." in error for error in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
