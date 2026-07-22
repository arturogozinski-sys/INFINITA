#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministyczny raport kondycji kanonu INFINITA.

Generuje raport Markdown i JSON. Kończy się kodem 1 wyłącznie wtedy,
gdy występuje co najmniej jeden błąd twardy. Ostrzeżenia nie blokują CI.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rdzen.parser import parsuj_plik  # noqa: E402
from rdzen.walidator import Walidator  # noqa: E402


def _wzgledna(sciezka: str | Path, root: Path) -> str:
    path = Path(sciezka).resolve()
    try:
        return path.relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def analizuj(kanon: Path, schemat: Path) -> dict:
    walidator = Walidator(str(schemat))
    pliki = sorted(kanon.rglob("*.md"))
    wezly: list[dict] = []
    krawedzie: list[tuple[str, str, str]] = []
    bledy: list[str] = []
    ostrzezenia: list[str] = []

    for plik in pliki:
        try:
            wezel, lokalne_krawedzie = parsuj_plik(str(plik))
        except Exception as exc:
            bledy.append(f"{_wzgledna(plik, ROOT)}: błąd parsowania: {exc}")
            continue

        wezly.append(wezel)
        krawedzie.extend(lokalne_krawedzie)
        bledy.extend(walidator.sprawdz_wezel(wezel))

        ident = str(wezel.get("id", ""))
        if plik.stem != ident:
            bledy.append(
                f"{_wzgledna(plik, ROOT)}: nazwa pliku '{plik.stem}' != id '{ident}'"
            )
        if wezel.get("typ") == "hipoteza":
            bledy.append(f"{ident}: typ hipoteza nie może znajdować się w kanonie")
        if wezel.get("status_epistemiczny") not in walidator.s["status_epistemiczny"][
            "dozwolone_w_kanonie"
        ]:
            bledy.append(
                f"{ident}: status_epistemiczny '{wezel.get('status_epistemiczny', '')}' "
                "nie jest dozwolony w kanonie"
            )

    pliki_wg_id: dict[str, list[str]] = defaultdict(list)
    for wezel in wezly:
        pliki_wg_id[str(wezel.get("id", ""))].append(
            _wzgledna(str(wezel.get("sciezka", "")), ROOT)
        )
    for ident, sciezki in sorted(pliki_wg_id.items()):
        if len(sciezki) > 1:
            bledy.append(
                f"{ident}: zduplikowany identyfikator w plikach: {', '.join(sorted(sciezki))}"
            )

    ids = set(pliki_wg_id)
    wychodzace = Counter()
    przychodzace = Counter()
    for zrodlo, cel, _typ in krawedzie:
        wychodzace[zrodlo] += 1
        przychodzace[cel] += 1
        if cel not in ids:
            ostrzezenia.append(f"martwe odwołanie: {zrodlo} -> {cel}")

    osierocone = sorted(
        ident for ident in ids if wychodzace[ident] == 0 and przychodzace[ident] == 0
    )
    for ident in osierocone:
        ostrzezenia.append(f"węzeł osierocony: {ident}")

    typy = Counter(str(w.get("typ", "")) for w in wezly)
    statusy = Counter(str(w.get("status_epistemiczny", "")) for w in wezly)
    centra = sorted(
        (
            {
                "id": ident,
                "przychodzace": przychodzace[ident],
                "wychodzace": wychodzace[ident],
                "razem": przychodzace[ident] + wychodzace[ident],
            }
            for ident in ids
        ),
        key=lambda x: (-x["razem"], x["id"]),
    )[:10]

    return {
        "wersja_schematu": walidator.wersja_schematu,
        "liczba_plikow": len(pliki),
        "liczba_wezlow": len(wezly),
        "liczba_krawedzi": len(krawedzie),
        "typy": dict(sorted(typy.items())),
        "statusy_epistemiczne": dict(sorted(statusy.items())),
        "bledy_twarde": sorted(set(bledy)),
        "ostrzezenia": sorted(set(ostrzezenia)),
        "martwe_odwolania": sorted(
            set(o for o in ostrzezenia if o.startswith("martwe odwołanie:"))
        ),
        "wezly_osierocone": osierocone,
        "centra_grafu": centra,
    }


def render_markdown(raport: dict) -> str:
    linie = [
        "# RAPORT KONDYCJI INFINITA",
        "",
        f"- Wersja schematu: `{raport['wersja_schematu']}`",
        f"- Pliki kanonu: **{raport['liczba_plikow']}**",
        f"- Węzły: **{raport['liczba_wezlow']}**",
        f"- Krawędzie: **{raport['liczba_krawedzi']}**",
        f"- Błędy twarde: **{len(raport['bledy_twarde'])}**",
        f"- Ostrzeżenia: **{len(raport['ostrzezenia'])}**",
        "",
        "## Typy węzłów",
        "",
    ]
    for typ, liczba in raport["typy"].items():
        linie.append(f"- `{typ}`: {liczba}")

    linie.extend(["", "## Błędy twarde", ""])
    linie.extend(
        [f"- {blad}" for blad in raport["bledy_twarde"]]
        or ["Brak błędów twardych."]
    )

    linie.extend(["", "## Ostrzeżenia", ""])
    linie.extend(
        [f"- {ostrzezenie}" for ostrzezenie in raport["ostrzezenia"]]
        or ["Brak ostrzeżeń."]
    )

    linie.extend(["", "## Centra grafu", "", "| id | przychodzące | wychodzące | razem |", "|---|---:|---:|---:|"])
    for centrum in raport["centra_grafu"]:
        linie.append(
            f"| {centrum['id']} | {centrum['przychodzace']} | "
            f"{centrum['wychodzace']} | {centrum['razem']} |"
        )
    linie.append("")
    return "\n".join(linie)


def zapisz(raport: dict, md: Path, json_path: Path) -> None:
    md.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(render_markdown(raport), encoding="utf-8")
    json_path.write_text(
        json.dumps(raport, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kanon", type=Path, default=ROOT / "kanon")
    parser.add_argument("--schemat", type=Path, default=ROOT / "schemat_grafu.json")
    parser.add_argument("--md", type=Path, default=ROOT / "RAPORT_KONDYCJI.md")
    parser.add_argument(
        "--json", dest="json_path", type=Path, default=ROOT / "raport_kondycji.json"
    )
    args = parser.parse_args(argv)

    raport = analizuj(args.kanon, args.schemat)
    zapisz(raport, args.md, args.json_path)
    print(
        f"Raport kondycji: {len(raport['bledy_twarde'])} błędów twardych, "
        f"{len(raport['ostrzezenia'])} ostrzeżeń"
    )
    return 1 if raport["bledy_twarde"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
