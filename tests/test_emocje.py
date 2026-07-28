# -*- coding: utf-8 -*-
import json
from pathlib import Path
import tempfile
import unittest

from rdzen.emocje import (
    BladModeluEmocji,
    DekoderEmocji,
    sprawdz_manifest,
    waliduj_model,
)


ROOT = Path(__file__).resolve().parents[1]


class TestModelEmocji(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dekoder = DekoderEmocji.z_aktywnej_wersji(ROOT)

    def test_model_ma_dwanascie_wymiarow_i_czternascie_rodzin(self):
        self.assertEqual(len(self.dekoder.model["wymiary"]), 12)
        self.assertEqual(len(self.dekoder.model["rodziny"]), 14)

    def test_strach(self):
        wynik = self.dekoder.dekoduj(
            {
                "wplyw": ["zagrozenie_bezpieczenstwa_lub_integralnosci"],
                "kierunek_dzialania": ["ucieczka"],
                "warunek_domkniecia": ["nieokreslony"],
            }
        )
        self.assertEqual(wynik.wynik, "strach")

    def test_poczucie_winy(self):
        wynik = self.dekoder.dekoduj(
            {
                "przedmiot_oceny": ["wlasne_dzialanie"],
                "sprawstwo": ["wlasne"],
                "wplyw": ["naruszenie_normy"],
                "zakres_przypisania": ["czyn"],
                "kierunek_dzialania": ["naprawa"],
            }
        )
        self.assertEqual(wynik.wynik, "poczucie_winy")

    def test_jednoznaczne_przejscie_kazdej_rodziny(self):
        przypadki = {
            "strach": {
                "wplyw": ["zagrozenie_bezpieczenstwa_lub_integralnosci"],
                "kierunek_dzialania": ["ucieczka"],
            },
            "zlosc": {
                "wplyw": ["przeszkoda_w_dazeniu_do_celu"],
                "mozliwosc_kontroli": ["mozliwa"],
                "kierunek_dzialania": ["konfrontacja"],
            },
            "smutek": {
                "wplyw": ["utrata_lub_niedostepnosc"],
                "czas": ["dokonane"],
                "mozliwosc_kontroli": ["brak"],
                "kierunek_dzialania": ["wycofanie"],
            },
            "radosc": {
                "wplyw": ["osiagniecie_lub_korzysc"],
                "kierunek_dzialania": ["powtorzenie"],
            },
            "wstret": {
                "wplyw": ["skazenie_lub_naruszenie_integralnosci_ciala"],
                "kierunek_dzialania": ["oczyszczenie"],
            },
            "zaskoczenie": {
                "zgodnosc_z_przewidywaniem": ["niezgodne"],
                "wplyw": ["brak_istotnego_wplywu"],
                "kierunek_dzialania": ["orientacja"],
            },
            "wstyd": {
                "przedmiot_oceny": ["wlasne_ja"],
                "wplyw": ["naruszenie_normy"],
                "zakres_przypisania": ["cala_osoba"],
                "kierunek_dzialania": ["ukrycie"],
            },
            "poczucie_winy": {
                "przedmiot_oceny": ["wlasne_dzialanie"],
                "sprawstwo": ["wlasne"],
                "wplyw": ["naruszenie_normy"],
                "zakres_przypisania": ["czyn"],
                "kierunek_dzialania": ["naprawa"],
            },
            "zazenowanie": {
                "przedmiot_oceny": ["wlasne_dzialanie"],
                "struktura_relacji": ["ekspozycja_spoleczna"],
                "wplyw": ["brak_istotnego_wplywu"],
                "zakres_przypisania": ["czyn"],
                "kierunek_dzialania": ["korekta_zachowania"],
            },
            "duma": {
                "wplyw": ["osiagniecie_lub_korzysc"],
                "sprawstwo": ["wlasne"],
                "kierunek_dzialania": ["ujawnienie_osiagniecia"],
            },
            "wdziecznosc": {
                "przedmiot_oceny": ["inna_osoba"],
                "sprawstwo": ["innej_osoby"],
                "struktura_relacji": ["interakcja_spoleczna"],
                "wplyw": ["osiagniecie_lub_korzysc"],
                "ocena_intencji": ["pozytywna"],
                "kierunek_dzialania": ["podziekowanie"],
            },
            "zawisc": {
                "przedmiot_oceny": ["zasob_lub_pozycja"],
                "struktura_relacji": ["porownanie_spoleczne"],
                "wplyw": ["przeszkoda_w_dazeniu_do_celu"],
                "kierunek_dzialania": ["poprawa_wlasnej_pozycji"],
            },
            "zazdrosc": {
                "przedmiot_oceny": ["relacja"],
                "struktura_relacji": ["zagrozenie_wiezi"],
                "wplyw": ["zagrozenie_wiezi"],
                "czas": ["aktualne"],
                "kierunek_dzialania": ["ochrona_wiezi"],
            },
            "pogarda": {
                "przedmiot_oceny": ["inna_osoba"],
                "wplyw": ["naruszenie_normy"],
                "zakres_przypisania": ["cala_osoba"],
                "stabilnosc_oceny": ["stala"],
                "kierunek_dzialania": ["wykluczenie"],
            },
        }
        for oczekiwana, dane in przypadki.items():
            with self.subTest(rodzina=oczekiwana):
                self.assertEqual(
                    self.dekoder.dekoduj(dane).wynik,
                    oczekiwana,
                )

    def test_dzialanie_rozdziela_dume_i_radosc(self):
        wynik = self.dekoder.dekoduj(
            {
                "wplyw": ["osiagniecie_lub_korzysc"],
                "sprawstwo": ["wlasne"],
                "kierunek_dzialania": ["ujawnienie_osiagniecia"],
            }
        )
        self.assertEqual(set(wynik.po_syntezie), {"duma", "radosc"})
        self.assertEqual(wynik.wynik, "duma")

    def test_konflikt_bez_kierunku(self):
        wynik = self.dekoder.dekoduj(
            {
                "wplyw": ["osiagniecie_lub_korzysc"],
                "sprawstwo": ["wlasne"],
                "kierunek_dzialania": ["nieokreslony"],
            }
        )
        self.assertEqual(
            wynik.wynik, "nierozstrzygniety_konflikt_kandydatow"
        )

    def test_brak_kandydata_po_dzialaniu(self):
        wynik = self.dekoder.dekoduj(
            {
                "wplyw": ["skazenie_lub_naruszenie_integralnosci_ciala"],
                "kierunek_dzialania": ["podtrzymanie"],
            }
        )
        self.assertEqual(wynik.po_syntezie, ("wstret",))
        self.assertEqual(
            wynik.wynik, "nierozstrzygniety_brak_pasujacej_rodziny"
        )

    def test_domkniecie_jest_jawnym_adapterem(self):
        dane = {
            "wplyw": ["zagrozenie_bezpieczenstwa_lub_integralnosci"],
            "kierunek_dzialania": ["ucieczka"],
            "warunek_domkniecia": ["wygasanie"],
        }
        bez_oceny = self.dekoder.dekoduj(dane)
        self.assertTrue(bez_oceny.ocena_domkniecia_wymagana)
        ze_sprzecznoscia = self.dekoder.dekoduj(
            dane, {"strach": "sprzeczne"}
        )
        self.assertEqual(
            ze_sprzecznoscia.wynik,
            "nierozstrzygniety_brak_pasujacej_rodziny",
        )

    def test_wartosc_nieokreslona_nie_miesza_sie_z_okreslona(self):
        with self.assertRaises(BladModeluEmocji):
            self.dekoder.dekoduj(
                {"czas": ["dokonane", "nieokreslony"]}
            )

    def test_warunek_wykluczajacy_pozostaje_nieaktywny(self):
        model = json.loads(json.dumps(self.dekoder.model))
        model["rodziny"]["strach"]["warunki_wykluczajace"] = {}
        with self.assertRaises(BladModeluEmocji):
            waliduj_model(model)

    def test_manifest_aktywnej_wersji(self):
        self.assertEqual(sprawdz_manifest(ROOT), [])


if __name__ == "__main__":
    unittest.main()
