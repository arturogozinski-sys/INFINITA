#!/usr/bin/env python3
"""Buduje deterministyczny pakiet repozytorium dla zewnętrznego modelu Claude.

Pakiet zawiera aktualny stan repozytorium bez danych technicznych Git,
cache, środowisk lokalnych, sekretów i poprzednich archiwów. W katalogu
głównym pakietu powstaje CLAUDE_SNAPSHOT.yaml z pełnym SHA źródłowym.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import subprocess
import sys
import zipfile

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
}

EXCLUDED_NAMES = {
    ".env",
    ".env.local",
    ".DS_Store",
}

EXCLUDED_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".zip",
}


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def should_include(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if path.name in EXCLUDED_NAMES:
        return False
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_manifest(sha: str, branch: str, generated_at: str) -> str:
    return "\n".join(
        [
            "format: infinita-claude-snapshot",
            "wersja_formatu: 1",
            "repozytorium: arturogozinski-sys/INFINITA",
            f"branch: {yaml_quote(branch)}",
            f"commit_bazowy: {yaml_quote(sha)}",
            f"wygenerowano_utc: {yaml_quote(generated_at)}",
            "zrodlo_prawdy: github-master",
            "zasady:",
            "  - nie zakladaj istnienia nowszego stanu",
            "  - wszystkie zmiany odnos do commit_bazowy",
            "  - nie zmieniaj statusow epistemicznych bez decyzji operatora",
            "  - wynik zwroc z HANDOFF.yaml oraz lista zmienionych plikow",
            "  - przy rozjezdzie SHA zatrzymaj prace i zglos brak wspolnego stanu",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="dist")
    args = parser.parse_args()

    root = Path(git("rev-parse", "--show-toplevel")).resolve()
    sha = git("rev-parse", "HEAD")
    branch = os.environ.get("GITHUB_REF_NAME") or git("rev-parse", "--abbrev-ref", "HEAD")
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

    output_dir = (root / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"INFINITA_CLAUDE_{sha[:12]}.zip"

    files = sorted(
        path for path in root.rglob("*") if should_include(path, root)
    )

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("CLAUDE_SNAPSHOT.yaml", build_manifest(sha, branch, generated_at))
        for path in files:
            archive.write(path, path.relative_to(root).as_posix())

    print(output_path)
    print(f"files={len(files)}")
    print(f"commit={sha}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(exc.stderr, file=sys.stderr)
        raise SystemExit(exc.returncode) from exc
