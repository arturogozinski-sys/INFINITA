#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Odtwarza dokładną paczkę modelu ENC v3 z części Base64 i sprawdza SHA-256.

Użycie:
    python narzedzia/model_energetyczny_enc_v3/odtworz_paczke.py
    python narzedzia/model_energetyczny_enc_v3/odtworz_paczke.py --cel /tmp/model_enc_v3

Skrypt korzysta wyłącznie z biblioteki standardowej. Nie ufa nazwom ani
kolejności plików poza jawnym manifestem poniżej. Każda rozbieżność kończy
proces kodem innym niż zero.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ZIP_SHA256 = "558c05999563b30429adad92709fe2c5680dd1cbe6e78a9c2404ab8ff058f52c"
BASE64_SHA256 = "0f711f8052471a10385709a532e1b10a97c5cb43761916c6497570ebbf3315f2"

PLIKI_SHA256 = {
    "rdzen.py": "5c0b7ca3808d21032ef330f0b2920a704fe6a66d73eb912bae56d8ceddfdc48d",
    "przebieg.py": "141572c86a6e9b21f179e3ee8b0952e21ffc70c42b87d7a3ae58bdd36b024ca1",
    "rownowagi.py": "5a587ab3411aa09a46321a645cfb97ccfe0d6fd7fcbc126cd2535f8d212e5f6c",
    "dobowy.py": "5935a6ce6f5792e17f9b0d6978d10a514ee8a89b4c1505e103741579e7e81841",
    "RAPORT_E0_KUMULACJA_v3.md": "bc52baa1338b8d563082c907e693039434828f16374059fe854df63d0c78a927",
    "PRZEBIEG_PELNY.txt": "e95686f59a3a9590052c4e5447a7b66b944304dee123b8a260eb8a45c5a9b359",
}


def sha256_bytes(dane: bytes) -> str:
    return hashlib.sha256(dane).hexdigest()


def sha256_file(sciezka: Path) -> str:
    h = hashlib.sha256()
    with sciezka.open("rb") as plik:
        for blok in iter(lambda: plik.read(1024 * 1024), b""):
            h.update(blok)
    return h.hexdigest()


def znajdz_repo(start: Path) -> Path:
    for kandydat in (start, *start.parents):
        if (kandydat / "00_FUNDAMENT" / "FUNDAMENT.md").is_file():
            return kandydat
    raise RuntimeError("Nie znaleziono katalogu głównego repozytorium INFINITA.")


def odtworz(repo: Path, cel: Path, zachowaj_zip: bool = False) -> Path:
    katalog_czesci = repo / "robocze" / "model_energetyczny_enc_v3" / "paczka"
    czesci = sorted(katalog_czesci.glob("model_enc_v3.zip.b64.part-*"))
    if [p.name for p in czesci] != [f"model_enc_v3.zip.b64.part-{i:02d}" for i in range(8)]:
        raise RuntimeError(f"Niepełny lub nieoczekiwany zestaw części: {[p.name for p in czesci]}")

    tekst_b64 = "".join(p.read_text(encoding="ascii").strip() for p in czesci)
    b64_sha = sha256_bytes(tekst_b64.encode("ascii"))
    if b64_sha != BASE64_SHA256:
        raise RuntimeError(f"SHA-256 Base64 niezgodne: {b64_sha} != {BASE64_SHA256}")

    try:
        dane_zip = base64.b64decode(tekst_b64, validate=True)
    except Exception as exc:
        raise RuntimeError(f"Niepoprawne Base64: {exc}") from exc

    zip_sha = sha256_bytes(dane_zip)
    if zip_sha != ZIP_SHA256:
        raise RuntimeError(f"SHA-256 ZIP niezgodne: {zip_sha} != {ZIP_SHA256}")

    if cel.exists():
        shutil.rmtree(cel)
    cel.mkdir(parents=True)

    with tempfile.TemporaryDirectory(prefix="enc_v3_") as tymczasowy:
        zip_path = Path(tymczasowy) / "model_enc_v3.zip"
        zip_path.write_bytes(dane_zip)
        with zipfile.ZipFile(zip_path) as archiwum:
            nazwy = sorted(archiwum.namelist())
            oczekiwane = sorted(PLIKI_SHA256)
            if nazwy != oczekiwane:
                raise RuntimeError(f"Nieoczekiwana zawartość ZIP: {nazwy}; oczekiwano: {oczekiwane}")
            archiwum.extractall(cel)
        if zachowaj_zip:
            (cel / "model_enc_v3.zip").write_bytes(dane_zip)

    for nazwa, oczekiwany_sha in PLIKI_SHA256.items():
        sciezka = cel / nazwa
        faktyczny_sha = sha256_file(sciezka)
        if faktyczny_sha != oczekiwany_sha:
            raise RuntimeError(f"SHA-256 {nazwa} niezgodne: {faktyczny_sha} != {oczekiwany_sha}")

    return cel


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cel", type=Path, default=Path("/tmp/model_enc_v3"))
    parser.add_argument("--zachowaj-zip", action="store_true")
    args = parser.parse_args()

    try:
        repo = znajdz_repo(Path(__file__).resolve())
        wynik = odtworz(repo, args.cel.resolve(), args.zachowaj_zip)
    except Exception as exc:
        print(f"BŁĄD: {exc}", file=sys.stderr)
        return 1

    print(f"OK: odtworzono i zweryfikowano paczkę w {wynik}")
    print(f"ZIP SHA-256: {ZIP_SHA256}")
    for nazwa in sorted(PLIKI_SHA256):
        print(f"{PLIKI_SHA256[nazwa]}  {nazwa}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
