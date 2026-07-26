import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
KANON = ROOT / "kanon"


def read(doc_id: str) -> str:
    return (KANON / f"{doc_id}.md").read_text(encoding="utf-8")


class TestFrameKlasyfikacja(unittest.TestCase):
    def test_frame_is_connected_across_norm_mechanism_index_and_process(self):
        self.assertIn("ukrytego założenia pytania", read("S003"))
        self.assertIn("zawłaszczenie ramy interpretacyjnej", read("M043").lower())
        self.assertIn("FRAME", read("I006"))
        self.assertIn("FRAME / narzucona rama", read("P008"))

    def test_frame_subtypes_are_defined_and_routed(self):
        i006 = read("I006")
        p008 = read("P008").lower().replace("_", " ")
        expected = {
            "ZAŁOŻENIE",
            "ETYKIETA",
            "MOTYW",
            "WINA",
            "PRESJA",
            "FAŁSZYWA_ALTERNATYWA",
            "MORALIZACJA",
        }
        for subtype in expected:
            with self.subTest(subtype=subtype):
                self.assertIn(subtype, i006)
                self.assertIn(subtype.lower().replace("_", " "), p008)

    def test_frame_composite_result_is_not_an_eighth_subtype(self):
        m043 = read("M043")
        i006 = read("I006")
        p008 = read("P008")
        subtype_section = i006.split("## Podtypy FRAME", 1)[1].split(
            "## Wynik złożony FRAME", 1
        )[0]
        self.assertNotIn("ZAWŁASZCZENIE_RAMY", subtype_section)
        self.assertIn("wynik, nie podtyp", i006)
        self.assertIn("Jest skutkiem funkcjonalnym całej wypowiedzi", m043)
        self.assertIn("ocenić osobno wynik `ZAWŁASZCZENIE_RAMY`", p008)

    def test_frame_does_not_automatically_mean_false_or_manipulative(self):
        self.assertIn("nie rozstrzyga jeszcze, że rama jest fałszywa", read("I006"))
        self.assertIn(
            "nie oznacza automatycznie manipulacji ani fałszu", read("P008")
        )
        self.assertIn("Rama może być uzasadniona", read("M043"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
