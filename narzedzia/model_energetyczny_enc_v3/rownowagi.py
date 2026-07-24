# -*- coding: utf-8 -*-
"""Analiza wielogałęziowych punktów równowagi rdzenia.

Jeden mechanizm numeryczny dla całej analizy:
    - rozwiązanie F(x) = (dE/dt, dN/dt, dC/dt) = 0 metodą Newtona
      z jakobianem numerycznym i kontrolą residuum,
    - klasyfikacja stabilności przez wartości własne jakobianu,
    - lokalizacja punktów siodło-węzeł przez bisekcję na liczbie równowag,
      z weryfikacją det(J) -> 0 w znalezionym punkcie.

Brak całkowania w czasie. Brak przycinania. Brak zależności od warunku
początkowego ani od horyzontu.

OGRANICZENIE EPISTEMICZNE
    Wyniki dotyczą OBECNEJ POSTACI RÓWNAŃ i OBECNEJ PARAMETRYZACJI.
    Bistabilność i histereza są hipotezą strukturalną modelu, nie
    stwierdzeniem empirycznym o człowieku.
"""
from dataclasses import replace

import numpy as np

from rdzen import Parametry, Stan, pochodne

TOL_RESIDUUM = 1e-12
MAX_ITER = 200
EPS_JAKOBIAN = 1e-7
TOL_DUPLIKAT = 1e-6
MARGINES_DZIEDZINY = 1e-9


def F(x, K, p):
    """Prawa strona rdzenia jako wektor. Zależy wyłącznie od (E,N,C,K)."""
    dE, dN, dC, _, _ = pochodne(Stan(E=x[0], N=x[1], C=x[2]), K, p)
    return np.array([dE, dN, dC])


def jakobian(x, K, p, eps=EPS_JAKOBIAN):
    """Jakobian numeryczny, różnice centralne."""
    J = np.zeros((3, 3))
    for j in range(3):
        krok = eps * max(1.0, abs(x[j]))
        xp = x.copy(); xp[j] += krok
        xm = x.copy(); xm[j] -= krok
        J[:, j] = (F(xp, K, p) - F(xm, K, p)) / (2.0 * krok)
    return J


def w_dziedzinie(x, p):
    E, N, C = x
    return (-MARGINES_DZIEDZINY <= E <= p.E_max + MARGINES_DZIEDZINY
            and N >= -MARGINES_DZIEDZINY
            and -MARGINES_DZIEDZINY <= C <= 1.0 + MARGINES_DZIEDZINY)


def newton(x0, K, p):
    """Newton z tłumieniem. Zwraca (x, residuum) albo (None, None)."""
    x = np.array(x0, dtype=float)
    for _ in range(MAX_ITER):
        f = F(x, K, p)
        r = float(np.linalg.norm(f))
        if r < TOL_RESIDUUM:
            return x, r
        J = jakobian(x, K, p)
        try:
            krok = np.linalg.solve(J, -f)
        except np.linalg.LinAlgError:
            return None, None
        # tłumienie: przyjmij największy krok zmniejszający residuum
        alfa = 1.0
        for _ in range(40):
            kand = x + alfa * krok
            if np.linalg.norm(F(kand, K, p)) < r:
                break
            alfa *= 0.5
        else:
            return None, None
        x = x + alfa * krok
    f = F(x, K, p)
    r = float(np.linalg.norm(f))
    return (x, r) if r < TOL_RESIDUUM else (None, None)


def klasyfikuj(x, K, p):
    """Zwraca (wartosci_wlasne, stabilny, det_J)."""
    J = jakobian(x, K, p)
    w = np.linalg.eigvals(J)
    return w, bool(np.all(w.real < 0.0)), float(np.linalg.det(J))


def rownowagi(K, p=None, gestosc=4):
    """Wszystkie równowagi wewnętrzne dla danego K. Multi-start + deduplikacja."""
    p = p or Parametry()
    starty = []
    for E in np.linspace(0.02, 0.98, gestosc):
        for N in (0.01, 0.3, 1.2, 3.0, 7.0):
            for C in np.linspace(0.02, 0.98, gestosc):
                starty.append((E, N, C))
    znalezione = []
    for x0 in starty:
        x, r = newton(x0, K, p)
        if x is None or not w_dziedzinie(x, p):
            continue
        if any(np.linalg.norm(x - y[0]) < TOL_DUPLIKAT for y in znalezione):
            continue
        w, stab, detJ = klasyfikuj(x, K, p)
        znalezione.append((x, r, w, stab, detJ))
    znalezione.sort(key=lambda y: y[0][0])          # rosnąco po E
    return znalezione


def licz_rownowagi(K, p=None, gestosc=4):
    return len(rownowagi(K, p, gestosc))


def bisekcja_siodlo_wezel(K_lewy, K_prawy, p=None, tol=1e-8, gestosc=4):
    """Lokalizuje K, przy którym zmienia się liczba równowag.

    Zwraca (K_srodek, polowa_przedzialu, liczba_lewa, liczba_prawa, iteracje).
    """
    p = p or Parametry()
    nl = licz_rownowagi(K_lewy, p, gestosc)
    npr = licz_rownowagi(K_prawy, p, gestosc)
    if nl == npr:
        return None
    it = 0
    while K_prawy - K_lewy > tol and it < 200:
        sr = 0.5 * (K_lewy + K_prawy)
        if licz_rownowagi(sr, p, gestosc) == nl:
            K_lewy = sr
        else:
            K_prawy = sr
        it += 1
    return 0.5 * (K_lewy + K_prawy), 0.5 * (K_prawy - K_lewy), nl, npr, it


def znajdz_oba_siodla(p=None, gestosc=4, tol=1e-8):
    """Skan zgrubny + bisekcja obu punktów siodło-węzeł."""
    p = p or Parametry()
    siatka = np.linspace(0.05, 0.45, 41)
    liczby = [(float(K), licz_rownowagi(float(K), p, gestosc)) for K in siatka]
    przejscia = []
    for (K1, n1), (K2, n2) in zip(liczby, liczby[1:]):
        if n1 != n2:
            przejscia.append((K1, K2, n1, n2))
    wyniki = []
    for K1, K2, n1, n2 in przejscia:
        r = bisekcja_siodlo_wezel(K1, K2, p, tol, gestosc)
        if r:
            wyniki.append(r)
    return liczby, wyniki


def det_J_w_punkcie(K, p=None, gestosc=6):
    """Najmniejszy |det J| wśród równowag — miara bliskości siodła-węzła."""
    p = p or Parametry()
    r = rownowagi(K, p, gestosc)
    if not r:
        return None
    return min(abs(y[4]) for y in r)


def test_odpornosci(nazwy_parametrow, wzgledna=0.05, p=None, gestosc=3):
    """Lokalny test odporności: czy bistabilność przeżywa małe perturbacje.

    NIE jest to kalibracja. Zmieniamy po jednym parametrze o +/- `wzgledna`
    i sprawdzamy, czy nadal istnieje zakres K z trzema równowagami.
    """
    p = p or Parametry()
    wyniki = []
    for nazwa in nazwy_parametrow:
        for znak, etykieta in ((1.0, '+'), (-1.0, '−')):
            wart = getattr(p, nazwa)
            pp = replace(p, **{nazwa: wart * (1.0 + znak * wzgledna)})
            _, siodla = znajdz_oba_siodla(pp, gestosc=gestosc, tol=1e-6)
            if len(siodla) >= 2:
                dolny = min(s[0] for s in siodla)
                gorny = max(s[0] for s in siodla)
                wyniki.append((nazwa, etykieta, True, dolny, gorny))
            else:
                wyniki.append((nazwa, etykieta, False, None, None))
    return wyniki
