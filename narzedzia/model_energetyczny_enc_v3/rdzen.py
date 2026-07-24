# -*- coding: utf-8 -*-

"""Rdzeń dynamiczny modelu energetycznego — wersja graniczna v0.3.

Zakres wg MODEL_ENERGETYCZNY_SCALENIE_I_ERRATY_v0.2, sekcja 13.
Jeden układ, trzy zmienne stanu, jedno wejście na granicy.

Ω=1 jest progiem KLASYFIKACJI w warstwie odczytu — nie przełącza żadnego
równania. Progi bifurkacyjne rdzenia (punkty siodło-węzeł) to osobny obiekt,
wyznaczany w module rownowagi.py.
Druga strona reprezentowana wyłącznie przez sygnał graniczny.

Nazwy emocji nie występują w tym module. Celowo.
"""
import math
from dataclasses import dataclass, field


# ─────────────────────────────────────────────────────────────────────────────
# Parametry
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Parametry:
    """Stałe układu. Rozdzielone na trzy skale szybkości."""

    # --- skala szybka: napięcie ---
    phi: float = 1.00      # przepustowość nominalna przetwarzania
    rho: float = 0.60      # tempo rozładowania czynnego (wymaga C i E)
    rho_0: float = 0.12    # tempo rozpraszania biernego (nie wymaga C ani E)
    E_h: float = 0.25      # próg połówkowy dostępności zasobu (Michaelis)

    # --- skala średnia: zasób ---
    r: float = 0.30        # tempo regeneracji czynnej (wymaga C)
    r_0: float = 0.035     # bazowa regeneracja homeostatyczna (patrz opis w pochodne)
    c_phi: float = 0.35    # koszt jednostki przetworzonego obciążenia
    c_N: float = 0.12      # koszt utrzymywania jednostki napięcia
    c_0: float = 0.02      # koszt bazowy
    N_r: float = 1.50      # skala hamowania regeneracji przez napięcie
    E_max: float = 1.00

    # --- skala wolna: zdolność przepływu ---
    gamma: float = 0.020   # tempo odbudowy C
    delta: float = 0.045   # tempo degradacji C
    N_c: float = 1.00      # skala napięcia degradującego C

    # --- próg ---
    N_ref: float = 1.20    # napięcie odniesienia dla wskaźnika przeciążenia

    # --- warstwa wejścia (ślady, nie stan rdzenia — patrz §11) ---
    tau_minus: float = 8.0   # czas zaniku śladu po epizodzie
    tau_plus: float = 4.0    # czas zaniku obciążenia wyprzedzającego
    kappa_minus: float = 1.0
    kappa_plus: float = 1.0

    # --- bramka epizodu ---
    K_bazowe: float = 0.05   # obciążenie tła poza epizodem
    prog_epizodu: float = 0.15


@dataclass
class Stan:
    """Stan rdzenia. Trzy zmienne — nic więcej nie przekracza szwu."""
    E: float = 1.00
    N: float = 0.00
    C: float = 1.00

    def jako_krotka(self):
        return (self.E, self.N, self.C)


# ─────────────────────────────────────────────────────────────────────────────
# Funkcje pomocnicze — wszystkie zależne od stanu
# ─────────────────────────────────────────────────────────────────────────────

def g(E: float, p: Parametry) -> float:
    """Dostępność zasobu operacyjnego. Nasycenie typu Michaelisa.

    g(0) = 0: przy braku dostępnego zasobu nie ma wewnętrznego przetworzenia
    obciążenia, nie ma rozładowania czynnego i nie ma odbudowy C.
    Nie oznacza to braku zachowania zewnętrznego — model nie zawiera zmiennej
    wykonania zewnętrznego i o zachowaniu nie orzeka.

    g(E) bramkuje również drenaż E, co czyni brzeg E=0 niezmienniczym:
    nie można wydać zasobu, którego nie ma.
    """
    E = max(0.0, E)
    return E / (E + p.E_h)


def h(N: float, p: Parametry) -> float:
    """Hamowanie regeneracji przez napięcie. h→1 przy N→0, h→0 przy N≫N_r."""
    return 1.0 / (1.0 + max(0.0, N) / p.N_r)


def przepustowosc(s: Stan, p: Parametry) -> float:
    """Ile obciążenia układ jest w stanie przetworzyć w jednostce czasu.

    Iloczyn trzech czynników: przepustowość nominalna, zdolność przepływu,
    dostępność zasobu. Zerowanie któregokolwiek zeruje całość.
    """
    return p.phi * s.C * g(s.E, p)


def przetworzone(K: float, s: Stan, p: Parametry) -> float:
    """Strumień faktycznie przetworzony. Gładkie nasycenie zamiast min().

    Φ → K przy małym obciążeniu (wszystko przechodzi).
    Φ → Φ_max przy dużym (przepustowość jest granicą).
    """
    K = max(0.0, K)
    phi_max = przepustowosc(s, p)
    if phi_max <= 1e-12:
        return 0.0
    # KOREKTA K3: nasycenie tanh zamiast harmonicznego.
    # Harmoniczne blokowało ~39% obciążenia 0,50 przy zapasie przepustowości
    # 0,78 — układ produkował napięcie mimo wystarczającej zdolności.
    # tanh(x) ≈ x − x³/3, więc przy K ≪ Φ_max przechodzi praktycznie wszystko,
    # a nasycenie włącza się dopiero w okolicy przepustowości nominalnej.
    return phi_max * math.tanh(K / phi_max)


# ─────────────────────────────────────────────────────────────────────────────
# Równania — prawe strony zależą od stanu, nie od samego czasu
# ─────────────────────────────────────────────────────────────────────────────

def pochodne(s: Stan, K: float, p: Parametry):
    """Zwraca (dE/dt, dN/dt, dC/dt, Φ, B).

    Prawe strony rdzenia zależą WYŁĄCZNIE od aktualnego (E, N, C, K).
    Funkcja jest czysta: brak stanu modułowego, brak pamięci wywołań.
    Warstwa przygotowania wejścia (SladyWejscia: S_minus, S_plus) może
    przechowywać osobne ślady — nie należą one do rdzenia i wpływają na
    dynamikę wyłącznie przez wartość K.

    Domknięcie sprzężenia zwrotnego:
        K → B → N → (koszt + hamowanie) → E → g(E) → Φ → B
    Pętla jest zamknięta. Eskalacja wynika z równań, nie z katalogu.
    """
    Phi = przetworzone(K, s, p)
    B = max(0.0, K - Phi)                       # obciążenie zablokowane

    # napięcie: przyrost z blokady, ubytek dwoma kanałami rozładowania.
    # Czynny wymaga zdolności przepływu i dostępnego zasobu.
    # Bierny — rozpraszanie niezależne od C i E — działa zawsze.
    # Kanał bierny ogranicza N z góry: N* <= K / rho_0.
    N = max(0.0, s.N)
    U_czynne = p.rho * s.C * g(s.E, p) * N
    U_bierne = p.rho_0 * N
    dN = B - U_czynne - U_bierne

    # zasób: regeneracja minus koszty.
    # r*C  — regeneracja czynna, wymaga zdolności przepływu.
    # r_0  — bazowa regeneracja homeostatyczna: niezależna od C, aktywna
    #        TAKŻE podczas obciążenia, hamowana przez N przez h(N).
    #        Nie reprezentuje odpoczynku. Okno odpoczynku albo samoregulacji
    #        jest reprezentowane przez obniżenie K, nie przez r_0.
    # Drenaż bramkowany przez g(E): przy E=0 koszty nie są pobierane,
    # więc brzeg pozostaje niezmienniczy. Koszt przechodzi wtedy do N i C.
    R = (p.r * s.C + p.r_0) * (1.0 - s.E / p.E_max) * h(s.N, p)
    dE = R - p.c_phi * Phi - g(s.E, p) * (p.c_N * N + p.c_0)

    # zdolność przepływu: odbudowa vs degradacja
    odbudowa = p.gamma * (1.0 - s.C) * g(s.E, p) * h(s.N, p)
    degradacja = p.delta * s.C * (N / p.N_c)
    dC = odbudowa - degradacja

    return dE, dN, dC, Phi, B


def omega(s: Stan, p: Parametry) -> float:
    """Jeden wskaźnik przeciążenia. Ω > 1 oznacza przekroczenie.

    Licznik: napięcie do udźwignięcia.
    Mianownik: ile układ jest w stanie udźwignąć w OBECNYM stanie.

    Spadek C albo E zwiększa podatność bez dokładania osobnych progów.
    Zastępuje N_kryt, E_min i C_min jedną wielkością bezwymiarową.
    """
    pojemnosc = p.N_ref * s.C * g(s.E, p)
    if pojemnosc <= 1e-9:
        return float('inf')
    return max(0.0, s.N) / pojemnosc


# ─────────────────────────────────────────────────────────────────────────────
# Warstwa wejścia — ślady przeszłości i prognozy
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class SladyWejscia:
    """Stany ukryte warstwy przygotowania wejścia, NIE rdzenia.

    Napędzane wyłącznie obserwablami epizodu. Brak sprzężenia zwrotnego
    od stanu rdzenia — dzięki temu szew pozostaje jednokierunkowy.
    """
    S_minus: float = 0.0   # ślad niedomkniętych epizodów przeszłych
    S_plus: float = 0.0    # obciążenie wyprzedzające

    def krok(self, dt: float, p: Parametry, zastrzyk_minus=0.0, zastrzyk_plus=0.0):
        self.S_minus += zastrzyk_minus - dt * self.S_minus / p.tau_minus
        self.S_plus += zastrzyk_plus - dt * self.S_plus / p.tau_plus
        self.S_minus = max(0.0, self.S_minus)
        self.S_plus = max(0.0, self.S_plus)


# wagi mapowania u → K₀. Wszystkie składowe u wskazują ten sam kierunek:
# wyższa wartość = większe obciążenie. Mieszane znaki to pułapka kalibracyjna.
WAGI = {
    'intensywnosc':      0.40,
    'nieprzewidywalnosc': 0.20,
    'presja_czasowa':    0.15,
    'brak_wzajemnosci':  0.15,
    'brak_wyjscia':      0.20,
    'niedomkniecie':     0.00,   # nie obciąża w trakcie — zasila ślad S₋
}

SKLADOWE_U = list(WAGI.keys())


def mapuj(u: dict) -> float:
    """u → K₀. Liniowa matryca sprzężenia (§10).

    Nieliniowość celowo NIE siedzi tutaj. Jest w rdzeniu: nasycenie
    przepustowości, zależność od g(E), h(N) i próg Ω.
    """
    return sum(WAGI[k] * float(u.get(k, 0.0)) for k in WAGI)


def obciazenie_calkowite(u_biezace, slady: SladyWejscia, p: Parametry,
                         obciazenie_bierne: float = 0.0) -> float:
    """K = K₀ + κ₋S₋ + κ₊S₊ + obciążenie bierne.

    Obciążenie bierne to kanał dla somatyki, snu, pogody, trawienia.
    Nie jest interakcją, ale przekracza tę samą granicę — więc wchodzi
    tym samym interfejsem (errata E5).
    """
    K0 = mapuj(u_biezace) if u_biezace else 0.0
    return (K0
            + p.kappa_minus * slady.S_minus
            + p.kappa_plus * slady.S_plus
            + obciazenie_bierne
            + p.K_bazowe)


# ─────────────────────────────────────────────────────────────────────────────
# Całkowanie
# ─────────────────────────────────────────────────────────────────────────────

def krok_rk4(s: Stan, K: float, p: Parametry, dt: float) -> Stan:
    """Runge-Kutta 4. rzędu. Stabilniejsze niż Euler przy szybkiej dynamice N."""

    def f(st):
        dE, dN, dC, _, _ = pochodne(st, K, p)
        return dE, dN, dC

    def przesun(st, d, wsp):
        return Stan(st.E + wsp * d[0], st.N + wsp * d[1], st.C + wsp * d[2])

    k1 = f(s)
    k2 = f(przesun(s, k1, dt / 2))
    k3 = f(przesun(s, k2, dt / 2))
    k4 = f(przesun(s, k3, dt))

    E = s.E + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
    N = s.N + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    C = s.C + dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])

    return _osłoń(E, N, C, p)


# ─────────────────────────────────────────────────────────────────────────────
# Osłona numeryczna — NIE realizuje dynamiki
# ─────────────────────────────────────────────────────────────────────────────

TOLERANCJA_OSLONY = 1e-9

class NaruszenieDziedziny(RuntimeError):
    """Korekta przekroczyła tolerancję — dziedzina nie jest niezmiennicza."""


class LicznikOslony:
    """Zlicza aktywacje osłony i pilnuje, by pozostała osłoną błędu zaokrąglenia.

    Dziedzina jest niezmiennicza analitycznie (patrz dowód w raporcie), więc
    każda korekta większa niż TOLERANCJA_OSLONY oznacza błąd — nie mechanikę.
    """
    def __init__(self):
        self.aktywacje = 0
        self.max_korekta = 0.0

    def zglos(self, wielkosc: float, nazwa: str, tolerancja: float):
        if wielkosc <= 0.0:
            return
        self.aktywacje += 1
        self.max_korekta = max(self.max_korekta, wielkosc)
        if wielkosc > tolerancja:
            raise NaruszenieDziedziny(
                f"{nazwa}: korekta {wielkosc:.3e} > tolerancja {tolerancja:.1e}. "
                "Osłona nie może realizować dynamiki."
            )

    def raport(self) -> str:
        return (f"aktywacje={self.aktywacje}, "
                f"maks. korekta={self.max_korekta:.3e}, "
                f"tolerancja={TOLERANCJA_OSLONY:.1e}")


LICZNIK = LicznikOslony()


def _osłoń(E, N, C, p):
    LICZNIK.zglos(-E, "E < 0", TOLERANCJA_OSLONY)
    LICZNIK.zglos(E - p.E_max, "E > E_max", TOLERANCJA_OSLONY)
    LICZNIK.zglos(-N, "N < 0", TOLERANCJA_OSLONY)
    LICZNIK.zglos(-C, "C < 0", TOLERANCJA_OSLONY)
    LICZNIK.zglos(C - 1.0, "C > 1", TOLERANCJA_OSLONY)
    return Stan(E=min(p.E_max, max(0.0, E)), N=max(0.0, N), C=min(1.0, max(0.0, C)))


# ─────────────────────────────────────────────────────────────────────────────
# Detektor niespójności — kanał równoległy (§7, E6)
# ─────────────────────────────────────────────────────────────────────────────

def detektor_D(deklaracja: dict, trend: dict) -> float:
    """Porównuje deklarowany kierunek zmian z policzonym.

    Deklaracja i trend to słowniki o kluczach 'E', 'N', 'C' i wartościach
    w {-1, 0, +1}. D ∈ [0,1]: 0 = pełna zgodność, 1 = pełne przeciwieństwo.

    D NIE wraca do dynamiki. Nie jest oceną moralną. Jest resztą między
    dwoma kanałami danych.
    """
    if not deklaracja:
        return float('nan')
    osie = ['E', 'N', 'C']
    suma = sum(abs(deklaracja.get(o, 0) - trend.get(o, 0)) for o in osie)
    return suma / (2.0 * len(osie))
