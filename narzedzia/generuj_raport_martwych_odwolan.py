#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generuje raport martwych odwołań bez efektów ubocznych poza wskazanym plikiem."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rdzen.parser import zbuduj_indeks  # noqa: E402
from rdzen.repozytorium import IndeksSQLite  # noqa: E402

KANON = ROOT / "kanon"
SCHEMAT = ROOT / "schemat_grafu.json"
REJESTR = ROOT / "00_FUNDAMENT" / "KLASYFIKACJA_MARTWYCH_ODWOLAN.json"
WYJSCIE = ROOT / "00_FUNDAMENT" / "BRAKUJACE_ODWOLANIA.md"
KLASY = {"planowany", "archiwalny", "zewnetrzny", "blad"}


def zbierz_martwe_odwolania(kanon: Path, schemat: Path) -> dict[str, list[str]]:
    indeks = IndeksSQLite(":memory:")
    try:
        zbuduj_indeks(str(kanon), indeks, str(schemat))
        martwe = indeks.martwe_krawedzie()
    finally:
        indeks.close()

    wg_cel: dict[str, list[str]] = defaultdict(list)
    for krawedz in martwe:
        wg_cel[krawedz["cel"]].append(krawedz["zrodlo"])
    return {cel: sorted(zrodla) for cel, zrodla in sorted(wg_cel.items())}


def wczytaj_rejestr(path: Path) -> dict:
    if not path.exists():
        return {"wpisy": {}}
    with path.open(encoding="utf-8") as plik:
        return json.load(plik)


def ocen_wpis(cel: str, wpis: dict | None, dzis: dt.date) -> tuple[str, str, str]:
    if not wpis:
        return "nierozstrzygniete", "BRAK", "BLOCKER: brak wpisu w rejestrze"

    klasa = str(wpis.get("klasa", "nierozstrzygniete"))
    termin = str(wpis.get("termin", "BRAK"))
    if klasa not in KLASY and klasa != "nierozstrzygniete":
        return klasa, termin, "BLOCKER: nieznana klasa"

    if klasa == "blad":
        return klasa, termin, "BLOCKER"

    try:
        data_terminu = dt.date.fromisoformat(termin)
    except ValueError:
        return klasa, termin, "BLOCKER: niepoprawny termin"

    if dzis > data_terminu:
        return klasa, termin, "BLOCKER: termin minął"
    return klasa, termin, "otwarte"


def renderuj(
    wg_cel: dict[str, list[str]],
    rejestr: dict,
    dzis: dt.date,
) -> tuple[str, list[str]]:
    wpisy = rejestr.get("wpisy", {})
    blokery: list[str] = []
    liczba_krawedzi = sum(len(zrodla) for zrodla in wg_cel.values())
    linie = [
        "# Brakujące odwołania (martwe krawędzie w kanon/)",
        "",
        "Raport jest generowany mechanicznie. Klasyfikacja nie zmienia kanonu; "
        "wiąże brakujący cel z jawną decyzją i terminem.",
        "",
        f"Razem martwych krawędzi: **{liczba_krawedzi}**, "
        f"unikalnych celów: **{len(wg_cel)}**.",
        "",
        "| cel | ile | źródła | klasa | termin | stan |",
        "|---|---:|---|---|---|---|",
    ]

    for cel, zrodla in wg_cel.items():
        klasa, termin, stan = ocen_wpis(cel, wpisy.get(cel), dzis)
        if stan.startswith("BLOCKER"):
            blokery.append(f"{cel}: {klasa}: {stan}")
        linie.append(
            f"| {cel} | {len(zrodla)} | {', '.join(zrodla)} | "
            f"{klasa} | {termin} | {stan} |"
        )

    nieaktualne = sorted(set(wpisy) - set(wg_cel))
    if nieaktualne:
        linie.extend(
            [
                "",
                "## Wpisy do zamknięcia",
                "",
                "Cele obecne w rejestrze, które nie są już martwymi odwołaniami: "
                + ", ".join(nieaktualne)
                + ".",
            ]
        )
    linie.append("")
    return "\n".join(linie), blokery


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kanon", type=Path, default=KANON)
    parser.add_argument("--schemat", type=Path, default=SCHEMAT)
    parser.add_argument("--rejestr", type=Path, default=REJESTR)
    parser.add_argument("--output", type=Path, default=WYJSCIE)
    parser.add_argument(
        "--check",
        action="store_true",
        help="porównaj raport z plikiem wyjściowym i niczego nie zapisuj",
    )
    parser.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    args = parser.parse_args(argv)

    wg_cel = zbierz_martwe_odwolania(args.kanon, args.schemat)
    tekst, blokery = renderuj(wg_cel, wczytaj_rejestr(args.rejestr), args.today)
    if args.check:
        aktualny = (
            args.output.read_text(encoding="utf-8") if args.output.exists() else None
        )
        if aktualny != tekst:
            blokery.append(f"{args.output}: raport jest nieaktualny")
        print(f"Sprawdzono {args.output}")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(tekst, encoding="utf-8", newline="\n")
        print(
            f"Zapisano {args.output} "
            f"({len(wg_cel)} celów, {sum(map(len, wg_cel.values()))} martwych krawędzi)"
        )
    for blocker in blokery:
        print(f"BLOCKER: {blocker}", file=sys.stderr)
    return 1 if blokery else 0


if __name__ == "__main__":
    raise SystemExit(main())
