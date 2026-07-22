# -*- coding: utf-8 -*-
"""Walidator schematu SCHEMAT_GRAFU v1.0."""
import re, json

class Walidator:
    def __init__(self, sciezka_schematu):
        with open(sciezka_schematu, encoding='utf-8') as f:
            self.s = json.load(f)
        self.wzorzec_id = re.compile(self.s['system_identyfikatorow']['wzorzec'])
        self.prefiksy = self.s['system_identyfikatorow']['prefiksy']
        self.typy = self.s['typy_wezlow']

    @property
    def wersja_schematu(self):
        return self.s['wersja']

    def sprawdz_wezel(self, w: dict) -> list:
        naruszenia = []
        ident = w.get('id', '')
        typ = w.get('typ', '')
        if typ not in self.typy:
            naruszenia.append(f"{ident}: nieznany typ '{typ}'")
            return naruszenia
        spec = self.typy[typ]
        m = self.wzorzec_id.match(ident)
        if not m:
            naruszenia.append(f"{ident}: identyfikator niezgodny z wzorcem {self.s['system_identyfikatorow']['wzorzec']}")
        else:
            prefiks = m.group(1)
            if self.prefiksy.get(prefiks) != typ:
                naruszenia.append(f"{ident}: prefiks '{prefiks}' nie odpowiada typowi '{typ}' (oczekiwano prefiksu dla '{typ}')")
        for pole in spec['pola_wymagane']:
            if not w.get(pole):
                naruszenia.append(f"{ident}: brak wymaganego pola '{pole}' dla typu '{typ}'")
        se = w.get('status_epistemiczny', '')
        if se and se not in self.s['status_epistemiczny']['dozwolone']:
            naruszenia.append(f"{ident}: niedozwolony status_epistemiczny '{se}'")
        for pole, regula in spec.get('walidacja_dodatkowa', {}).items():
            wart = w.get(pole)
            if regula == "liczba 1-5":
                try:
                    if not (1 <= int(wart) <= 5):
                        naruszenia.append(f"{ident}: pole '{pole}' poza zakresem 1-5")
                except (ValueError, TypeError):
                    naruszenia.append(f"{ident}: pole '{pole}' nie jest liczbą 1-5")
        return naruszenia

    def sprawdz_wszystkie(self, wezly: list) -> list:
        out = []
        for w in wezly:
            out += self.sprawdz_wezel(w)
        return out
