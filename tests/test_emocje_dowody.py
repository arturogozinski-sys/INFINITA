# -*- coding: utf-8 -*-
from pathlib import Path
import re
import tempfile
import unittest

from rdzen.emocje import DekoderEmocji
from rdzen.emocje_dowody import wczytaj_korpus


ROOT = Path(__file__).resolve().parents[1]

MATERIAL_DEMONSTRACYJNY = """Przypadek demonstracyjny A

Wpływ: zagrożenie bezpieczeństwa lub integralności.
Kierunek działania: ochrona, unikanie albo ucieczka.
Domknięcie: nieokreślone.
"""

KLUCZ_DEMONSTRACYJNY = """Przypadek demonstracyjny A
Wynik: strach
Rodzina badana: strach
"""


class TestPublicznegoKontraktuAdapteraDowodow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.katalog_tymczasowy = tempfile.TemporaryDirectory()
        cls.katalog_repo = Path(cls.katalog_tymczasowy.name)
        katalog_serii = (
            cls.katalog_repo
            / "systemy"
            / "emocje"
            / "v1.0"
            / "dowody"
            / "serie"
            / "01"
        )
        katalog_serii.mkdir(parents=True)
        (katalog_serii / "MATERIAL_DEMONSTRACYJNY.md").write_text(
            MATERIAL_DEMONSTRACYJNY,
            encoding="utf-8",
        )
        (katalog_serii / "KLUCZ_DEMONSTRACYJNY.md").write_text(
            KLUCZ_DEMONSTRACYJNY,
            encoding="utf-8",
        )
        cls.rekordy = wczytaj_korpus(cls.katalog_repo)
        cls.dekoder = DekoderEmocji.z_aktywnej_wersji(ROOT)

    @classmethod
    def tearDownClass(cls):
        cls.katalog_tymczasowy.cleanup()

    def test_adapter_czyta_jawna_probke_demonstracyjna(self):
        self.assertEqual(len(self.rekordy), 1)
        self.assertEqual(self.rekordy[0].seria, "01")
        self.assertEqual(self.rekordy[0].nazwa, "Przypadek demonstracyjny A")

    def test_adapter_zachowuje_literalne_pola(self):
        rekord = self.rekordy[0]
        self.assertEqual(
            rekord.tekst_zrodlowy(),
            rekord.nazwa + "\n\n" + "\n".join(rekord.pola_surowe),
        )
        self.assertEqual(rekord.domkniecie_surowe, "nieokreślone")

    def test_probka_jest_wykonywalna_i_zgodna_z_jawnym_kluczem(self):
        rekord = self.rekordy[0]
        wynik = self.dekoder.dekoduj(rekord.dane)
        self.assertEqual(wynik.wynik, rekord.wynik_klucza)
        self.assertEqual(wynik.wynik, "strach")

    def test_powtorzenie_matrycy_ma_zgodny_klucz_i_wynik(self):
        katalog = (
            ROOT
            / "systemy"
            / "emocje"
            / "v1.0"
            / "dowody"
            / "powtorzenie_matrycy_podstawowej"
        )
        rodziny = {"strach", "złość", "smutek", "radość", "wstręt", "zaskoczenie"}
        klucz = {}
        for wiersz in (
            katalog / "KLUCZ_POWTORZENIA_WALIDACJI_MATRYCY_PODSTAWOWEJ.md"
        ).read_text(encoding="utf-8").splitlines():
            dopasowanie = re.fullmatch(r"([^:]+): (.+)", wiersz)
            if dopasowanie and dopasowanie.group(2) in rodziny:
                klucz[dopasowanie.group(1)] = dopasowanie.group(2)
        self.assertEqual(len(klucz), 24)
        self.assertEqual(
            {rodzina: list(klucz.values()).count(rodzina) for rodzina in rodziny},
            {rodzina: 4 for rodzina in rodziny},
        )

        wynik = {}
        for wiersz in (
            katalog / "WYNIK_POWTORZENIA_WALIDACJI_MATRYCY_PODSTAWOWEJ.md"
        ).read_text(encoding="utf-8").splitlines():
            kolumny = [kolumna.strip() for kolumna in wiersz.strip("|").split("|")]
            if len(kolumny) == 4 and kolumny[1] in rodziny:
                wynik[kolumny[0]] = tuple(kolumny[1:])
        self.assertEqual(
            wynik,
            {nazwa: (rodzina, rodzina, rodzina) for nazwa, rodzina in klucz.items()},
        )


if __name__ == "__main__":
    unittest.main()
