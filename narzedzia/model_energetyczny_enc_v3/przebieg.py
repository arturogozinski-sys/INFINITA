# -*- coding: utf-8 -*-
"""Symulator epizodyczny + kontrastowe przypadki testowe.

Kryterium zakończenia przebiegu: przez trzy zmienne stanu i próg warstwy
odczytu Ω=1 przechodzą realistyczne dane wejściowe, a model daje werdykt bez
nazwy emocji.

Ω=1 jest progiem KLASYFIKACJI w warstwie odczytu. Nie jest progiem
bifurkacyjnym i nie przełącza żadnego równania. Progi bifurkacyjne rdzenia
(punkty siodło-węzeł) są osobnym obiektem — patrz analiza równowag.
"""
from dataclasses import dataclass, field

from rdzen import (Parametry, Stan, SladyWejscia, detektor_D, krok_rk4,
                   obciazenie_calkowite, omega, pochodne, przepustowosc)


@dataclass
class Epizod:
    """Epizod sprzężenia. u — wektor obserwabli, wszystkie w skali 0–1."""
    start: float
    czas_trwania: float
    u: dict
    zapowiedziany_z_wyprzedzeniem: float = 0.0  # ile jednostek czasu wcześniej


@dataclass
class Scenariusz:
    nazwa: str
    opis: str
    stan_poczatkowy: Stan
    epizody: list = field(default_factory=list)
    obciazenie_bierne: object = 0.0   # stała albo funkcja czasu
    horyzont: float = 120.0
    dt: float = 0.05
    deklaracja: dict = None            # deklarowany kierunek zmian


def bierne(scen, t):
    ob = scen.obciazenie_bierne
    return ob(t) if callable(ob) else float(ob)


def symuluj(scen: Scenariusz, p: Parametry):
    """Zwraca listę migawek stanu w czasie."""
    s = Stan(**vars(scen.stan_poczatkowy))
    slady = SladyWejscia()
    historia = []
    t = 0.0
    wstrzyknieto_slad = set()
    zapowiedziano = set()
    n_krokow = int(scen.horyzont / scen.dt)

    for i in range(n_krokow + 1):
        # --- ustal, czy trwa epizod ---
        aktywny = None
        for idx, ep in enumerate(scen.epizody):
            if ep.start <= t < ep.start + ep.czas_trwania:
                aktywny = ep
                break

        # --- zastrzyki do śladów: najpierw sumujemy, potem JEDNO wywołanie ---
        # Poprzednio slady.krok() było wywoływane raz na każdy zastrzyk plus raz
        # bezwarunkowo, przez co w krokach z zastrzykiem zanik stosowano
        # wielokrotnie, a wynik zależał od kolejności epizodów w tablicy.
        zastrzyk_plus = 0.0
        zastrzyk_minus = 0.0

        # obciążenie wyprzedzające: zapowiedź nadchodzącego epizodu
        for idx, ep in enumerate(scen.epizody):
            if idx in zapowiedziano or ep.zapowiedziany_z_wyprzedzeniem <= 0:
                continue
            if ep.start - ep.zapowiedziany_z_wyprzedzeniem <= t < ep.start:
                zastrzyk_plus += 0.5 * ep.u.get('intensywnosc', 0.0)
                zapowiedziano.add(idx)

        # ślad po epizodzie: zastrzyk proporcjonalny do niedomknięcia
        for idx, ep in enumerate(scen.epizody):
            koniec = ep.start + ep.czas_trwania
            if idx not in wstrzyknieto_slad and t >= koniec:
                zastrzyk_minus += (ep.u.get('niedomkniecie', 0.0)
                                   * ep.u.get('intensywnosc', 0.0))
                wstrzyknieto_slad.add(idx)

        slady.krok(scen.dt, p, zastrzyk_minus=zastrzyk_minus,
                   zastrzyk_plus=zastrzyk_plus)

        K = obciazenie_calkowite(aktywny.u if aktywny else None, slady, p,
                                 bierne(scen, t))
        dE, dN, dC, Phi, B = pochodne(s, K, p)
        Om = omega(s, p)

        historia.append({
            't': t, 'E': s.E, 'N': s.N, 'C': s.C, 'K': K, 'Phi': Phi, 'B': B,
            'Omega': Om, 'dE': dE, 'dN': dN, 'dC': dC,
            'tryb': 'epizod' if (aktywny or K > p.prog_epizodu) else 'baza',
        })

        s = krok_rk4(s, K, p, scen.dt)
        t += scen.dt

    return historia


# ─────────────────────────────────────────────────────────────────────────────
# Odczyt wyniku — bez nazw emocji
# ─────────────────────────────────────────────────────────────────────────────

def znak(x, prog=1e-3):
    return 1 if x > prog else (-1 if x < -prog else 0)


def werdykt(hist, p: Parametry, deklaracja=None):
    """Werdykt strukturalny. Żadna nazwa emocji nie występuje."""
    pierwszy, ostatni = hist[0], hist[-1]
    Om_max = max(h['Omega'] for h in hist)
    N_max = max(h['N'] for h in hist)
    czas_ponad = sum(1 for h in hist if h['Omega'] > 1.0) * (hist[1]['t'] - hist[0]['t'])
    przekroczenie = Om_max > 1.0

    # trend liczony na całym horyzoncie
    trend = {
        'E': znak(ostatni['E'] - pierwszy['E'], 0.02),
        'N': znak(ostatni['N'] - pierwszy['N'], 0.02),
        'C': znak(ostatni['C'] - pierwszy['C'], 0.005),
    }

    # czy układ wraca do bazy
    N_koniec = ostatni['N']
    powrot = N_koniec < 0.1 * max(N_max, 1e-9)

    D = detektor_D(deklaracja, trend) if deklaracja else float('nan')

    return {
        'E_koniec': ostatni['E'], 'N_koniec': N_koniec, 'C_koniec': ostatni['C'],
        'N_max': N_max, 'Omega_max': Om_max, 'przekroczenie': przekroczenie,
        'czas_ponad_progiem': czas_ponad, 'trend': trend, 'powrot_do_bazy': powrot,
        'D': D,
    }


def raport(scen: Scenariusz, p: Parametry):
    hist = symuluj(scen, p)
    w = werdykt(hist, p, scen.deklaracja)
    print(f"\n{'═' * 74}")
    print(f"  {scen.nazwa}")
    print(f"  {scen.opis}")
    print(f"{'═' * 74}")
    print(f"  start:  E={hist[0]['E']:.3f}  N={hist[0]['N']:.3f}  C={hist[0]['C']:.3f}")
    print(f"  koniec: E={w['E_koniec']:.3f}  N={w['N_koniec']:.3f}  C={w['C_koniec']:.3f}")
    print(f"  N_max={w['N_max']:.3f}   Ω_max={w['Omega_max']:.3f}"
          f"   próg przekroczony: {'TAK' if w['przekroczenie'] else 'nie'}"
          f"   czas ponad progiem: {w['czas_ponad_progiem']:.1f}")
    print(f"  trend: E{'+' if w['trend']['E']>0 else ('−' if w['trend']['E']<0 else '0')}"
          f"  N{'+' if w['trend']['N']>0 else ('−' if w['trend']['N']<0 else '0')}"
          f"  C{'+' if w['trend']['C']>0 else ('−' if w['trend']['C']<0 else '0')}"
          f"   powrót do bazy: {'tak' if w['powrot_do_bazy'] else 'NIE'}")
    if scen.deklaracja:
        print(f"  deklaracja: {scen.deklaracja}   →   D = {w['D']:.3f}")
    # przebieg skrócony
    print(f"\n  {'t':>6} {'K':>7} {'E':>7} {'N':>7} {'C':>7} {'Ω':>7}  tryb")
    krok = max(1, len(hist) // 14)
    for h in hist[::krok]:
        flaga = ' ⚠' if h['Omega'] > 1.0 else ''
        print(f"  {h['t']:6.1f} {h['K']:7.3f} {h['E']:7.3f} {h['N']:7.3f} "
              f"{h['C']:7.3f} {h['Omega']:7.3f}  {h['tryb']}{flaga}")
    return hist, w


# ─────────────────────────────────────────────────────────────────────────────
# TRZY KONTRASTOWE EPIZODY
# ─────────────────────────────────────────────────────────────────────────────

def u_wek(intensywnosc=0.0, nieprzewidywalnosc=0.0, presja_czasowa=0.0,
          brak_wzajemnosci=0.0, brak_wyjscia=0.0, niedomkniecie=0.0):
    return dict(intensywnosc=intensywnosc, nieprzewidywalnosc=nieprzewidywalnosc,
                presja_czasowa=presja_czasowa, brak_wzajemnosci=brak_wzajemnosci,
                brak_wyjscia=brak_wyjscia, niedomkniecie=niedomkniecie)


PRZYPADEK_1 = Scenariusz(
    nazwa="PRZYPADEK 1 — pojedynczy ostry epizod, zasoby dobre, domknięty",
    opis="Krótkie intensywne zdarzenie. Wysoka intensywność, pełne domknięcie.",
    stan_poczatkowy=Stan(E=0.95, N=0.05, C=1.00),
    epizody=[Epizod(start=10.0, czas_trwania=3.0,
                    u=u_wek(intensywnosc=0.95, nieprzewidywalnosc=0.7,
                            presja_czasowa=0.8, niedomkniecie=0.05))],
    horyzont=100.0,
    # deklaracja zgodna z przebiegiem: "napiecie zeszlo, zasoby w porzadku"
    deklaracja={'E': 0, 'N': -1, 'C': 0},
)

PRZYPADEK_2 = Scenariusz(
    nazwa="PRZYPADEK 2 — powtarzalne epizody niedomknięte, brak wyjścia",
    opis="Umiarkowana intensywność, wysokie niedomknięcie, brak możliwości wycofania.",
    stan_poczatkowy=Stan(E=0.90, N=0.10, C=1.00),
    epizody=[Epizod(start=8.0 + 12.0 * i, czas_trwania=4.0,
                    u=u_wek(intensywnosc=0.55, nieprzewidywalnosc=0.5,
                            presja_czasowa=0.3, brak_wzajemnosci=0.7,
                            brak_wyjscia=0.85, niedomkniecie=0.9),
                    zapowiedziany_z_wyprzedzeniem=3.0)
             for i in range(8)],
    horyzont=120.0,
    # deklaracja sprzeczna z przebiegiem: "odbudowuje sie, napiecie spada"
    deklaracja={'E': +1, 'N': -1, 'C': 0},
)

PRZYPADEK_3 = Scenariusz(
    nazwa="PRZYPADEK 3 — brak epizodów, obciążenie bierne narastające",
    opis="Somatyka i deficyt snu. Zero interakcji. Test: czy Ω łapie osunięcie bez napięcia.",
    stan_poczatkowy=Stan(E=0.85, N=0.05, C=1.00),
    epizody=[],
    obciazenie_bierne=lambda t: 0.10 + 0.0035 * t,
    horyzont=120.0,
    # deklaracja czesciowo trafna: "nic sie nie dzieje"
    deklaracja={'E': 0, 'N': 0, 'C': 0},
)

PRZYPADEK_4 = Scenariusz(
    nazwa="PRZYPADEK 4 — kontrola: ten sam epizod co w 1, ale C zdegradowane",
    opis="Identyczne wejście jak w przypadku 1. Różni się wyłącznie stan początkowy C.",
    stan_poczatkowy=Stan(E=0.95, N=0.05, C=0.35),
    epizody=[Epizod(start=10.0, czas_trwania=3.0,
                    u=u_wek(intensywnosc=0.95, nieprzewidywalnosc=0.7,
                            presja_czasowa=0.8, niedomkniecie=0.05))],
    horyzont=100.0,
    deklaracja={'E': 0, 'N': -1, 'C': +1},
)


if __name__ == '__main__':
    p = Parametry()
    for scen in (PRZYPADEK_1, PRZYPADEK_2, PRZYPADEK_3, PRZYPADEK_4):
        raport(scen, p)
