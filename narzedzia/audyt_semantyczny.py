#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lekki audyt semantyczny kanonu.

BŁĘDY zatrzymują CI: obiektywne rozjazdy metadanych i deklarowanych relacji.
OSTRZEŻENIA nie zatrzymują CI: sygnały mieszania kategorii, nadmiernego zakresu
lub regulatora pozostającego na peryferiach. Mają być widoczne, zanim dryf stanie
się nową tradycją projektu.
"""
from __future__ import annotations

import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KANON = ROOT / "kanon"
ID_RE = re.compile(r"\b[A-Z]{1,3}\d{3}\b")
H2_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
KROK_RE = re.compile(r"^##\s+Krok\s+(\d+)", re.MULTILINE | re.IGNORECASE)
NUMEROWANY_RE = re.compile(r"^(\d+)\.\s+", re.MULTILINE)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    block, body = parts[1], parts[2]
    meta: dict[str, object] = {}
    current = None
    for line in block.splitlines():
        if not line.strip():
            continue
        if re.match(r"^\s*-\s+", line):
            if current:
                meta.setdefault(current, [])
                if isinstance(meta[current], list):
                    meta[current].append(line.split("-", 1)[1].strip())
        elif ":" in line:
            key, value = line.split(":", 1)
            current = key.strip()
            meta[current] = value.strip() if value.strip() else []
    return meta, body


def ids_from_declared_links(body: str) -> set[str] | None:
    match = re.search(
        r"^Powiązania(?:\s+kanoniczne)?\s*:\s*(.+)$",
        body,
        re.MULTILINE | re.IGNORECASE,
    )
    if not match:
        return None
    return set(ID_RE.findall(match.group(1)))


def audit() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    docs: dict[str, dict] = {}
    outgoing: dict[str, set[str]] = {}
    incoming = Counter()

    for path in sorted(KANON.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        ident = str(meta.get("id", ""))
        typ = str(meta.get("typ", ""))
        refs = set(meta.get("odwolania", [])) if isinstance(meta.get("odwolania"), list) else set()
        docs[ident] = {"path": path, "typ": typ, "body": body, "meta": meta}
        outgoing[ident] = refs

        if path.stem != ident:
            errors.append(f"{path.relative_to(ROOT)}: nazwa pliku nie odpowiada id {ident}")

        declared = ids_from_declared_links(body)
        if declared is not None and declared != refs:
            errors.append(
                f"{ident}: Powiązania w treści {sorted(declared)} != odwolania YAML {sorted(refs)}"
            )

        lowered = body.lower()
        if "status operacyjny" in lowered or "op-" in lowered or "fn-" in lowered:
            errors.append(
                f"{ident}: używa starego/niejednoznacznego modelu statusu operacyjnego lub FN/OP"
            )

        headings = H2_RE.findall(body)
        heading_text = " | ".join(headings).lower()

        if typ == "zasada":
            if not re.search(r"\b(zasada|reguła)\b", heading_text):
                warnings.append(f"{ident}: zasada bez jawnej sekcji Zasada/Reguła")
            if "granica" not in heading_text:
                warnings.append(f"{ident}: zasada bez jawnej granicy stosowania")

        if typ == "mechanizm":
            if not re.search(r"\b(teza|definicja|punkt wyjścia)\b", heading_text):
                warnings.append(f"{ident}: mechanizm bez Tezy/Definicji/Punktu wyjścia")
            if re.search(r"^##\s+(Proces|Procedura)\b", body, re.MULTILINE | re.IGNORECASE):
                warnings.append(f"{ident}: mechanizm zawiera procedurę; możliwe mieszanie z typem P")
            if len(headings) >= 8:
                warnings.append(f"{ident}: {len(headings)} sekcji H2; możliwy dokument wielofunkcyjny")

        if typ == "proces":
            numbered = [int(n) for n in NUMEROWANY_RE.findall(body)]
            detailed = [int(n) for n in KROK_RE.findall(body)]
            if numbered and detailed and max(numbered) > max(detailed):
                warnings.append(
                    f"{ident}: deklaruje co najmniej {max(numbered)} kroków, rozwija tylko {max(detailed)}"
                )
            if not numbered and not detailed:
                warnings.append(f"{ident}: proces bez wykrywalnej sekwencji kroków")

        if typ == "indeks" and re.search(r"^##\s+Reguła\b", body, re.MULTILINE | re.IGNORECASE):
            warnings.append(f"{ident}: indeks zawiera regułę normatywną; rozważyć przeniesienie do S/P/Z")

    known = set(docs)
    for source, refs in outgoing.items():
        for target in refs:
            if target in known:
                incoming[target] += 1
            else:
                warnings.append(f"{source} -> {target}: brak celu w kanonie")

    for ident, doc in docs.items():
        if doc["typ"] in {"zasada", "specyfikacja"} and incoming[ident] == 0:
            warnings.append(
                f"{ident}: regulator typu {doc['typ']} bez odwołań przychodzących; możliwe peryferyjne położenie"
            )

    return sorted(set(errors)), sorted(set(warnings))


def main() -> int:
    errors, warnings = audit()
    for item in warnings:
        print(f"OSTRZEŻENIE: {item}")
    for item in errors:
        print(f"BŁĄD: {item}")
    print(f"Audyt semantyczny: {len(errors)} błędów, {len(warnings)} ostrzeżeń")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
