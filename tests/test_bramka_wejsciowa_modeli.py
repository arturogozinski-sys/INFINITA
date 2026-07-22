from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from narzedzia import raport_kondycji, raport_roznicowy


ROOT = Path(__file__).resolve().parent.parent
SCHEMAT = ROOT / "schemat_grafu.json"


def dokument(
    ident: str,
    *,
    typ: str = "mechanizm",
    status: str = "zweryfikowane",
    odwolania: tuple[str, ...] = (),
) -> str:
    refs = ""
    if odwolania:
        refs = "odwolania:\n" + "".join(f"  - {ref}\n" for ref in odwolania)
    return (
        "---\n"
        f"id: {ident}\n"
        f"typ: {typ}\n"
        f"tytul: Test {ident}\n"
        f"status_produkcyjny: kanon\n"
        f"status_epistemiczny: {status}\n"
        "wersja: 1.0\n"
        f"{refs}"
        "---\n"
        f"# {ident}\n\nTreść testowa wystarczająca do walidacji.\n"
    )


class RaportKondycjiAdwersarialnyTest(unittest.TestCase):
    def analizuj(self, pliki: dict[str, str]) -> dict:
        with TemporaryDirectory() as tmp:
            kanon = Path(tmp) / "kanon"
            kanon.mkdir()
            for nazwa, tresc in pliki.items():
                (kanon / nazwa).write_text(tresc, encoding="utf-8")
            return raport_kondycji.analizuj(kanon, SCHEMAT)

    def test_naruszenie_schematu_blokuje(self) -> None:
        raport = self.analizuj({"M001.md": dokument("M001", typ="nieznany")})
        self.assertTrue(any("nieznany typ" in b for b in raport["bledy_twarde"]))

    def test_duplikat_id_blokuje(self) -> None:
        raport = self.analizuj(
            {"M001.md": dokument("M001"), "M002.md": dokument("M001")}
        )
        self.assertTrue(
            any("zduplikowany identyfikator" in b for b in raport["bledy_twarde"])
        )

    def test_nazwa_pliku_rozna_od_id_blokuje(self) -> None:
        raport = self.analizuj({"M999.md": dokument("M001")})
        self.assertTrue(any("nazwa pliku" in b for b in raport["bledy_twarde"]))

    def test_hipoteza_w_kanonie_blokuje(self) -> None:
        raport = self.analizuj({"H001.md": dokument("H001", typ="hipoteza")})
        self.assertTrue(
            any("hipoteza nie może" in b for b in raport["bledy_twarde"])
        )

    def test_status_inny_niz_zweryfikowane_blokuje(self) -> None:
        raport = self.analizuj(
            {"M001.md": dokument("M001", status="propozycja")}
        )
        self.assertTrue(
            any("nie jest dozwolony w kanonie" in b for b in raport["bledy_twarde"])
        )

    def test_martwe_odwolanie_i_osierocenie_nie_blokuja(self) -> None:
        raport = self.analizuj(
            {
                "M001.md": dokument("M001", odwolania=("M999",)),
                "M002.md": dokument("M002"),
            }
        )
        self.assertEqual([], raport["bledy_twarde"])
        self.assertTrue(any("martwe odwołanie" in o for o in raport["ostrzezenia"]))
        self.assertIn("M002", raport["wezly_osierocone"])


class RaportRoznicowyBramkaTest(unittest.TestCase):
    def test_nieistniejacy_commit_jest_odrzucany(self) -> None:
        with self.assertRaises(RuntimeError):
            raport_roznicowy.sprawdz_bramke("commit-ktorego-nie-ma", "HEAD")

    def test_commit_docelowy_musi_byc_head(self) -> None:
        head = raport_roznicowy.pelny_sha("HEAD")
        rodzic = raport_roznicowy.git("rev-parse", "HEAD^")
        if rodzic == head:
            self.skipTest("repozytorium nie ma rodzica HEAD")
        with self.assertRaises(RuntimeError):
            raport_roznicowy.sprawdz_bramke(rodzic, rodzic)


if __name__ == "__main__":
    unittest.main()
