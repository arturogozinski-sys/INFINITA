#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Raport różnicowy dla modeli pracujących na repozytorium INFINITA.

Wymaga jawnego commita bazowego i docelowego. Commit docelowy musi odpowiadać
aktualnemu HEAD, a commit bazowy musi być jego przodkiem. Dzięki temu raport
nie udaje, że opisuje inny stan drzewa roboczego niż faktycznie odczytuje.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rdzen.parser import parsuj_plik  # noqa: E402

HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and proc.returncode != 0:
        komunikat = proc.stderr.strip() or proc.stdout.strip() or "nieznany błąd git"
        raise RuntimeError(komunikat)
    return proc.stdout.strip()


def pelny_sha(ref: str) -> str:
    return git("rev-parse", "--verify", f"{ref}^{{commit}}")


def sprawdz_bramke(od_ref: str, do_ref: str) -> tuple[str, str]:
    od_sha = pelny_sha(od_ref)
    do_sha = pelny_sha(do_ref)
    head_sha = pelny_sha("HEAD")
    if do_sha != head_sha:
        raise RuntimeError(
            f"commit docelowy {do_sha} nie odpowiada aktualnemu HEAD {head_sha}"
        )
    proc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", od_sha, do_sha],
        cwd=ROOT,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"commit bazowy {od_sha} nie jest przodkiem {do_sha}")
    return od_sha, do_sha


def zmienione_pliki(od_sha: str, do_sha: str) -> list[tuple[str, str]]:
    wynik = git("diff", "--name-status", od_sha, do_sha, "--")
    rekordy: list[tuple[str, str]] = []
    for linia in wynik.splitlines():
        if not linia.strip():
            continue
        pola = linia.split("\t")
        status = pola[0]
        sciezka = pola[-1]
        rekordy.append((status, sciezka))
    return rekordy


def zakresy_linii(od_sha: str, do_sha: str, sciezka: str) -> list[str]:
    diff = git("diff", "--unified=0", od_sha, do_sha, "--", sciezka)
    zakresy: list[str] = []
    for linia in diff.splitlines():
        match = HUNK_RE.match(linia)
        if not match:
            continue
        start = int(match.group(1))
        count = int(match.group(2) or "1")
        if count == 0:
            zakresy.append(f"po linii {start}")
        elif count == 1:
            zakresy.append(str(start))
        else:
            zakresy.append(f"{start}-{start + count - 1}")
    return zakresy


def graf_kanonu(kanon: Path) -> tuple[dict[str, str], dict[str, set[str]]]:
    sciezki: dict[str, str] = {}
    sasiedzi: dict[str, set[str]] = defaultdict(set)
    for plik in sorted(kanon.rglob("*.md")):
        wezel, krawedzie = parsuj_plik(str(plik))
        ident = str(wezel["id"])
        sciezki[ident] = plik.relative_to(ROOT).as_posix()
        for zrodlo, cel, _typ in krawedzie:
            sasiedzi[zrodlo].add(cel)
            sasiedzi[cel].add(zrodlo)
    return sciezki, sasiedzi


def buduj_raport(od_ref: str, do_ref: str, kanon: Path) -> str:
    od_sha, do_sha = sprawdz_bramke(od_ref, do_ref)
    zmiany = zmienione_pliki(od_sha, do_sha)
    sciezki_id, sasiedzi = graf_kanonu(kanon)
    id_po_sciezce = {sciezka: ident for ident, sciezka in sciezki_id.items()}

    bezposrednie_id = {
        id_po_sciezce[sciezka]
        for _status, sciezka in zmiany
        if sciezka in id_po_sciezce
    }
    sasiedztwo_id: set[str] = set()
    for ident in bezposrednie_id:
        sasiedztwo_id.update(sasiedzi.get(ident, set()))
    sasiedztwo_id -= bezposrednie_id

    do_czytania = {
        sciezka for _status, sciezka in zmiany if Path(sciezka).suffix in {".md", ".py", ".json", ".yml", ".yaml"}
    }
    do_czytania.update(
        sciezki_id[ident] for ident in sasiedztwo_id if ident in sciezki_id
    )
    wszystkie_kanoniczne = set(sciezki_id.values())
    nie_trzeba = sorted(wszystkie_kanoniczne - do_czytania)

    linie = [
        "# RAPORT RÓŻNICOWY DLA MODELU",
        "",
        "## Bramka commita",
        "",
        f"- Commit bazowy: `{od_sha}`",
        f"- Commit docelowy / HEAD: `{do_sha}`",
        "- Relacja: commit bazowy jest przodkiem commita docelowego",
        "",
        "## Dotknięte bezpośrednio",
        "",
    ]

    if not zmiany:
        linie.append("Brak zmian.")
    for status, sciezka in zmiany:
        zakresy = zakresy_linii(od_sha, do_sha, sciezka)
        opis_zakresu = ", ".join(zakresy) if zakresy else "brak aktualnych linii / plik usunięty"
        linie.append(f"- `{sciezka}` ({status}; linie: {opis_zakresu})")

    linie.extend(["", "## Sąsiedztwo jednego kroku w grafie", ""])
    if not sasiedztwo_id:
        linie.append("Brak sąsiadów wymagających dodatkowego sprawdzenia.")
    else:
        for ident in sorted(sasiedztwo_id):
            sciezka = sciezki_id.get(ident, "cel poza bieżącym kanonem")
            linie.append(f"- `{ident}` — `{sciezka}`")

    linie.extend(["", "## DO PRZECZYTANIA", ""])
    if do_czytania:
        for sciezka in sorted(do_czytania):
            linie.append(f"- `{sciezka}`")
    else:
        linie.append("Brak plików do przeczytania.")

    linie.extend(["", "## NIE trzeba czytać", ""])
    linie.append(
        f"Pozostałe pliki kanonu bez zmian i poza sąsiedztwem: **{len(nie_trzeba)}**."
    )
    for sciezka in nie_trzeba:
        linie.append(f"- `{sciezka}`")
    linie.append("")
    return "\n".join(linie)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--od", required=True, help="commit bazowy")
    parser.add_argument("--do", default="HEAD", help="commit docelowy; musi być HEAD")
    parser.add_argument("--kanon", type=Path, default=ROOT / "kanon")
    parser.add_argument(
        "--wyjscie", type=Path, default=ROOT / "RAPORT_ROZNICOWY.md"
    )
    args = parser.parse_args(argv)

    try:
        raport = buduj_raport(args.od, args.do, args.kanon)
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"Bramka commita odrzuciła zadanie: {exc}", file=sys.stderr)
        return 1

    args.wyjscie.parent.mkdir(parents=True, exist_ok=True)
    args.wyjscie.write_text(raport, encoding="utf-8")
    print(f"Zapisano {args.wyjscie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
