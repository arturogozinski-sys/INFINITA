#!/usr/bin/env python3
"""Buduje powtarzalny snapshot wyłącznie z zawartości wskazanego commita Git."""
from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path, PurePosixPath
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
EXCLUDED_NAMES = {".env", ".env.local", ".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".zip"}


def git(root: Path, *args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        text=text,
        encoding="utf-8" if text else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip() if text else result.stdout


def should_include(path: str) -> bool:
    rel = PurePosixPath(path)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if rel.name in EXCLUDED_NAMES:
        return False
    return rel.suffix.lower() not in EXCLUDED_SUFFIXES


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_manifest(sha: str, branch: str, generated_at: str) -> str:
    return "\n".join(
        [
            "format: infinita-claude-snapshot",
            "wersja_formatu: 2",
            "repozytorium: arturogozinski-sys/INFINITA",
            f"branch: {yaml_quote(branch)}",
            f"commit_bazowy: {yaml_quote(sha)}",
            f"czas_commita_utc: {yaml_quote(generated_at)}",
            "zrodlo_prawdy: git-commit",
            "zawartosc_working_tree: false",
            "zasady:",
            "  - wszystkie pliki pochodza wylacznie z commit_bazowy",
            "  - zmiany niezapisane i pliki niesledzone nie wchodza do pakietu",
            "  - przy rozjezdzie SHA zatrzymaj prace i zglos brak wspolnego stanu",
            "",
        ]
    )


def zip_info(name: str, timestamp: dt.datetime) -> zipfile.ZipInfo:
    safe_year = max(1980, timestamp.year)
    info = zipfile.ZipInfo(
        name,
        (safe_year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second),
    )
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    return info


def build_snapshot(root: Path, output_dir: Path, ref: str = "HEAD") -> Path:
    root = Path(str(git(root, "rev-parse", "--show-toplevel"))).resolve()
    sha = str(git(root, "rev-parse", f"{ref}^{{commit}}"))
    branch = os.environ.get("GITHUB_REF_NAME") or str(
        git(root, "rev-parse", "--abbrev-ref", ref)
    )
    commit_time_text = str(git(root, "show", "-s", "--format=%cI", sha))
    commit_time = dt.datetime.fromisoformat(commit_time_text).astimezone(dt.timezone.utc)
    generated_at = commit_time.replace(microsecond=0).isoformat()

    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"INFINITA_CLAUDE_{sha[:12]}.zip"

    raw_names = git(root, "ls-tree", "-r", "--name-only", "-z", sha, text=False)
    assert isinstance(raw_names, bytes)
    files = sorted(
        name.decode("utf-8")
        for name in raw_names.split(b"\0")
        if name and should_include(name.decode("utf-8"))
    )

    with zipfile.ZipFile(output_path, "w") as archive:
        manifest = build_manifest(sha, branch, generated_at).encode("utf-8")
        archive.writestr(zip_info("CLAUDE_SNAPSHOT.yaml", commit_time), manifest)
        for name in files:
            content = git(root, "show", f"{sha}:{name}", text=False)
            assert isinstance(content, bytes)
            archive.writestr(zip_info(name, commit_time), content)

    print(output_path)
    print(f"files={len(files)}")
    print(f"commit={sha}")
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--ref", default="HEAD")
    args = parser.parse_args(argv)
    build_snapshot(args.repo_root, args.output_dir, args.ref)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else exc.stderr
        print(stderr, file=sys.stderr)
        raise SystemExit(exc.returncode) from exc
