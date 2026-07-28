# -*- coding: utf-8 -*-
from collections import Counter
from pathlib import Path
import re
import unittest

from rdzen.emocje import DekoderEmocji
from rdzen.emocje_dowody import (
    etap_wyniku,
    ocen_zgodnosc_domkniecia,
    wczytaj_korpus,
)


ROOT = Path(__file__).resolve().parents[1]


class TestAdapterDowodowEmocji(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rekordy = wczytaj_korpus(ROOT)
        cls.dekoder = DekoderEmocji.z_aktywnej_wersji(ROOT)

    def test_adapter_czyta_wszystkie_trzysta_dziesiec_rekordow(self):
        self.assertEqual(
            Counter(rekord.seria for rekord in self.rekordy),
            {
                "01": 28,
                "02": 38,
                "03": 27,
                "04": 56,
                "05": 70,
                "06": 91,
            },
        )

    def test_adapter_zachowuje_literalne_pola(self):
        for rekord in self.rekordy:
            with self.subTest(seria=rekord.seria, nazwa=rekord.nazwa):
                self.assertEqual(
                    rekord.tekst_zrodlowy(),
                    rekord.nazwa + "\n\n" + "\n".join(rekord.pola_surowe),
                )
                self.assertTrue(rekord.domkniecie_surowe)

    def test_wszystkie_rekordy_sa_wykonywalne(self):
        for rekord in self.rekordy:
            with self.subTest(seria=rekord.seria, nazwa=rekord.nazwa):
                self.dekoder.dekoduj(rekord.dane)

    def test_zgodnosc_bez_semantycznego_testu_domkniecia(self):
        niezgodne = []
        for rekord in self.rekordy:
            wynik = self.dekoder.dekoduj(rekord.dane)
            if wynik.wynik != rekord.wynik_klucza:
                niezgodne.append((rekord.seria, rekord.nazwa))
                continue
            self.assertEqual(etap_wyniku(wynik), rekord.etap_klucza)
            if rekord.kandydaci_klucza:
                self.assertEqual(wynik.kandydaci, rekord.kandydaci_klucza)
        self.assertEqual(len(niezgodne), 28)
        self.assertEqual({seria for seria, _ in niezgodne}, {"05"})

    def test_pelna_zgodnosc_po_literalnym_tescie_domkniecia(self):
        for rekord in self.rekordy:
            with self.subTest(seria=rekord.seria, nazwa=rekord.nazwa):
                ocena = ocen_zgodnosc_domkniecia(
                    self.dekoder.model,
                    rekord,
                )
                wynik = self.dekoder.dekoduj(rekord.dane, ocena)
                self.assertEqual(wynik.wynik, rekord.wynik_klucza)
                self.assertEqual(etap_wyniku(wynik), rekord.etap_klucza)
                if rekord.kandydaci_klucza:
                    self.assertEqual(wynik.kandydaci, rekord.kandydaci_klucza)

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
        for wiersz in (katalog / "KLUCZ_POWTORZENIA_WALIDACJI_MATRYCY_PODSTAWOWEJ.md").read_text(
            encoding="utf-8"
        ).splitlines():
            dopasowanie = re.fullmatch(r"([^:]+): (.+)", wiersz)
            if dopasowanie and dopasowanie.group(2) in rodziny:
                klucz[dopasowanie.group(1)] = dopasowanie.group(2)
        self.assertEqual(len(klucz), 24)
        self.assertEqual(Counter(klucz.values()), {rodzina: 4 for rodzina in rodziny})

        wynik = {}
        for wiersz in (katalog / "WYNIK_POWTORZENIA_WALIDACJI_MATRYCY_PODSTAWOWEJ.md").read_text(
            encoding="utf-8"
        ).splitlines():
            kolumny = [kolumna.strip() for kolumna in wiersz.strip("|").split("|")]
            if len(kolumny) == 4 and kolumny[1] in rodziny:
                wynik[kolumny[0]] = tuple(kolumny[1:])
        self.assertEqual(
            wynik,
            {nazwa: (rodzina, rodzina, rodzina) for nazwa, rodzina in klucz.items()},
        )


if __name__ == "__main__":
    unittest.main()
