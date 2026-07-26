#!/usr/bin/env python3
"""Waliduje lekki kontrakt przekazania INFINITA bez zewnętrznych zależności."""
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

REQUIRED = {
    "format",
    "wersja_formatu",
    "repozytorium",
    "branch_bazowy",
    "commit_bazowy",
    "wykonawca",
    "data_utworzenia",
    "tryb",
    "zadanie.id",
    "zadanie.cel",
    "zadanie.zakres",
    "zadanie.poza_zakresem",
    "wynik.typ",
    "wynik.katalog_lub_plik",
    "wynik.pliki_zmienione",
    "walidacja.polecenia",
    "walidacja.testy_oczekiwane",
    "walidacja.wynik_deklarowany",
    "walidacja.drzewo_czyste_po_testach",
    "pochodzenie.dokumenty_nadrzedne",
    "pochodzenie.uwagi",
    "ograniczenia",
    "decyzje_wymagane_od_operatora",
}
PLACEHOLDERS = {"UZUPELNIJ", "UZUPELNIJ_PELNY_SHA", "YYYY-MM-DD"}
ENUMS = {
    "wykonawca": {"claude", "copilot", "gpt", "czlowiek"},
    "tryb": {"implementacja", "audyt", "symulacja", "synteza", "redakcja", "diagnoza"},
    "wynik.typ": {"snapshot", "patch", "raport"},
    "walidacja.wynik_deklarowany": {"nieuruchomione", "sukces", "blad", "czesciowy"},
}


def _scalar(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if value == "[]":
        return []
    if value == "null":
        return None
    if value in {"true", "false"}:
        return value == "true"
    if re.fullmatch(r"\d+", value):
        return int(value)
    return value


def parse_simple_yaml(text: str) -> dict[str, object]:
    """Czyta wyłącznie podzbiór YAML używany przez HANDOFF_TEMPLATE."""
    result: dict[str, object] = {}
    stack: list[tuple[int, str]] = []
    for number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if "\t" in raw[:indent]:
            raise ValueError(f"linia {number}: tabulator we wcięciu")
        stripped = raw.strip()
        while stack and stack[-1][0] >= indent:
            stack.pop()

        if stripped.startswith("- "):
            if not stack:
                raise ValueError(f"linia {number}: element listy bez klucza")
            path = ".".join(key for _, key in stack)
            current = result.setdefault(path, [])
            if not isinstance(current, list):
                raise ValueError(f"linia {number}: {path} nie jest listą")
            current.append(_scalar(stripped[2:]))
            continue

        if ":" not in stripped:
            raise ValueError(f"linia {number}: oczekiwano klucza YAML")
        key, value = stripped.split(":", 1)
        path = ".".join([*(item[1] for item in stack), key])
        if value.strip():
            if path in result and result[path] != []:
                raise ValueError(f"linia {number}: powtórzone pole {path}")
            result[path] = _scalar(value)
        else:
            result.setdefault(path, [])
            stack.append((indent, key))
    return result


def validate(data: dict[str, object], template: bool = False) -> list[str]:
    errors = [f"brak pola: {path}" for path in sorted(REQUIRED - set(data))]
    if errors or template:
        return errors

    if data["format"] != "infinita-handoff":
        errors.append("format musi mieć wartość infinita-handoff")
    if data["wersja_formatu"] != 1:
        errors.append("wersja_formatu musi mieć wartość 1")
    if not re.fullmatch(r"[0-9a-fA-F]{40}", str(data["commit_bazowy"])):
        errors.append("commit_bazowy musi być pełnym 40-znakowym SHA")

    for path in (
        "repozytorium",
        "branch_bazowy",
        "wykonawca",
        "data_utworzenia",
        "tryb",
        "zadanie.id",
        "zadanie.cel",
        "wynik.typ",
        "wynik.katalog_lub_plik",
        "walidacja.wynik_deklarowany",
    ):
        value = data[path]
        if not isinstance(value, str) or not value.strip() or value in PLACEHOLDERS:
            errors.append(f"{path}: wartość nieuzupełniona")

    try:
        dt.date.fromisoformat(str(data["data_utworzenia"]))
    except ValueError:
        errors.append("data_utworzenia musi mieć format YYYY-MM-DD")

    for path, allowed in ENUMS.items():
        if data[path] not in allowed:
            errors.append(f"{path}: wartość spoza dozwolonego zbioru")

    for path in ("zadanie.zakres", "walidacja.polecenia", "pochodzenie.dokumenty_nadrzedne"):
        if not isinstance(data[path], list) or not data[path]:
            errors.append(f"{path}: wymagana niepusta lista")
    for path in (
        "zadanie.poza_zakresem",
        "wynik.pliki_zmienione",
        "ograniczenia",
        "decyzje_wymagane_od_operatora",
    ):
        if not isinstance(data[path], list):
            errors.append(f"{path}: wymagana lista")

    if data["walidacja.wynik_deklarowany"] == "sukces":
        if not isinstance(data["walidacja.testy_oczekiwane"], int):
            errors.append("przy sukcesie testy_oczekiwane musi być liczbą")
        if data["walidacja.drzewo_czyste_po_testach"] is not True:
            errors.append("przy sukcesie drzewo_czyste_po_testach musi być true")

    for path in ("wynik.katalog_lub_plik",):
        value = Path(str(data[path]))
        if value.is_absolute() or ".." in value.parts:
            errors.append(f"{path}: ścieżka musi być względna i nie może zawierać ..")
    for path in ("zadanie.zakres", "zadanie.poza_zakresem", "wynik.pliki_zmienione"):
        values = data[path] if isinstance(data[path], list) else []
        for value in values:
            candidate = Path(str(value))
            if candidate.is_absolute() or ".." in candidate.parts:
                errors.append(f"{path}: niedozwolona ścieżka {value}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plik", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--template",
        action="store_true",
        help="sprawdź wyłącznie kompletność struktury szablonu",
    )
    args = parser.parse_args(argv)

    try:
        data = parse_simple_yaml(args.plik.read_text(encoding="utf-8"))
        errors = validate(data, template=args.template)
        if not args.template and not errors:
            commit = str(data["commit_bazowy"])
            check = subprocess.run(
                ["git", "-C", str(args.repo_root), "cat-file", "-e", f"{commit}^{{commit}}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if check.returncode:
                errors.append("commit_bazowy nie istnieje w lokalnym repozytorium")
    except (OSError, ValueError) as exc:
        errors = [str(exc)]

    for error in errors:
        print(f"BŁĄD HANDOFF: {error}", file=sys.stderr)
    if not errors:
        print(f"HANDOFF poprawny: {args.plik}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
