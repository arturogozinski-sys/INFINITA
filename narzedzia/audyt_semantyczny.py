#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audyt spójności i szczelności kanonu INFINITA."""
from __future__ import annotations

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
PREFIX_TYP = {
    "S": "specyfikacja", "M": "mechanizm", "P": "proces", "Z": "zasada",
    "E": "dowod", "C": "przypadek", "D": "dialog", "I": "indeks", "H": "hipoteza",
}
STOP = {"oraz", "jest", "nie", "dla", "przez", "jako", "tego", "który", "która", "które", "się", "czy", "przy", "system", "dokument"}


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
    match = re.search(r"^Powiązania(?:\s+kanoniczne)?\s*:\s*(.+)$", body, re.MULTILINE | re.IGNORECASE)
    return set(ID_RE.findall(match.group(1))) if match else None


def tokens(text: str) -> set[str]:
    words = re.findall(r"[a-ząćęłńóśźż]{4,}", text.lower())
    return {w for w in words if w not in STOP}


def audit(katalog: Path = KANON) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    docs: dict[str, dict] = {}
    outgoing: dict[str, set[str]] = {}
    incoming = Counter()
    fingerprints: dict[frozenset[str], list[str]] = defaultdict(list)

    for path in sorted(katalog.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        ident = str(meta.get("id", ""))
        typ = str(meta.get("typ", ""))
        refs = set(meta.get("odwolania", [])) if isinstance(meta.get("odwolania"), list) else set()

        if not ident:
            errors.append(f"{path.name}: brak id")
            continue
        if ident in docs:
            errors.append(f"{ident}: zduplikowany identyfikator semantyczny")
        docs[ident] = {"path": path, "typ": typ, "body": body, "meta": meta}
        outgoing[ident] = refs

        if path.stem != ident:
            errors.append(f"{path.name}: nazwa pliku nie odpowiada id {ident}")
        prefiks = re.match(r"^[A-Z]+", ident)
        expected = PREFIX_TYP.get(prefiks.group(0) if prefiks else "")
        if expected and typ != expected:
            errors.append(f"{ident}: typ {typ!r} nie zgadza się z prefiksem; oczekiwano {expected!r}")
        if meta.get("status_produkcyjny") != "kanon":
            errors.append(f"{ident}: plik w kanon/ ma status_produkcyjny != kanon")
        if meta.get("status_epistemiczny") != "zweryfikowane":
            errors.append(f"{ident}: plik w kanon/ ma status_epistemiczny != zweryfikowane")

        declared = ids_from_declared_links(body)
        if declared is not None and declared != refs:
            errors.append(f"{ident}: Powiązania w treści {sorted(declared)} != odwolania YAML {sorted(refs)}")

        lowered = body.lower()
        if ident != "S002" and ("status operacyjny" in lowered or "op-" in lowered or "fn-" in lowered):
            errors.append(f"{ident}: używa starego modelu statusu operacyjnego lub FN/OP")

        headings = H2_RE.findall(body)
        heading_text = " | ".join(headings).lower()
        if typ == "zasada":
            if not re.search(r"\b(zasada|reguła)\b", heading_text):
                warnings.append(f"{ident}: zasada bez sekcji Zasada/Reguła")
            if "granica" not in heading_text:
                warnings.append(f"{ident}: zasada bez granicy stosowania")
        if typ == "mechanizm":
            if not re.search(r"\b(teza|definicja|punkt wyjścia)\b", heading_text):
                warnings.append(f"{ident}: mechanizm bez Tezy/Definicji/Punktu wyjścia")
            if re.search(r"^##\s+(Proces|Procedura)\b", body, re.MULTILINE | re.IGNORECASE):
                warnings.append(f"{ident}: mechanizm zawiera procedurę; możliwe mieszanie z P")
            if len(headings) >= 8:
                warnings.append(f"{ident}: {len(headings)} sekcji H2; możliwy dokument wielofunkcyjny")
        if typ == "proces":
            numbered = [int(n) for n in NUMEROWANY_RE.findall(body)]
            detailed = [int(n) for n in KROK_RE.findall(body)]
            if numbered and detailed and max(numbered) > max(detailed):
                warnings.append(f"{ident}: deklaruje {max(numbered)} kroków, rozwija {max(detailed)}")
            if not numbered and not detailed:
                warnings.append(f"{ident}: proces bez wykrywalnej sekwencji kroków")
        if typ == "indeks" and re.search(r"^##\s+Reguła\b", body, re.MULTILINE | re.IGNORECASE):
            warnings.append(f"{ident}: indeks zawiera regułę normatywną")

        fp = frozenset(tokens(str(meta.get("tytul", "")) + " " + body))
        if len(fp) >= 8:
            fingerprints[fp].append(ident)

    known = set(docs)
    for source, refs in outgoing.items():
        for target in refs:
            if target in known:
                incoming[target] += 1
            else:
                warnings.append(f"{source} -> {target}: brak celu w kanonie")

    for ident, doc in docs.items():
        if doc["typ"] in {"zasada", "specyfikacja"} and incoming[ident] == 0:
            warnings.append(f"{ident}: regulator bez odwołań przychodzących; możliwe peryferyjne położenie")

    ids = sorted(docs)
    for i, left in enumerate(ids):
        a = tokens(str(docs[left]["meta"].get("tytul", "")) + " " + docs[left]["body"])
        if len(a) < 8:
            continue
        for right in ids[i + 1:]:
            b = tokens(str(docs[right]["meta"].get("tytul", "")) + " " + docs[right]["body"])
            if len(b) < 8:
                continue
            similarity = len(a & b) / len(a | b)
            if similarity >= 0.72:
                warnings.append(f"{left} ~ {right}: wysokie podobieństwo treści ({similarity:.0%}); możliwy dubel")

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
