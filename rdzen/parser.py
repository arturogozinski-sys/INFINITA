# -*- coding: utf-8 -*-
"""Parser kanonu (Proces produkcji wiedzy: PARSER czyta WYŁĄCZNIE kanon).
Markdown + front-matter YAML -> węzły + krawędzie -> indeks (przez warstwę abstrakcji).
Parser nie zna silnika bazy — dostaje obiekt RepozytoriumIndeksu.
Bez zależności zewnętrznych: minimalny parser YAML front-matter (klucz: wartość + listy).
"""
import os, re, glob

ID_RE = re.compile(r'^([A-Z]{1,3}\d{2,3})')

def _parse_frontmatter(tekst):
    """Minimalny YAML: bloki '---' na górze. Obsługuje klucz: wartosc oraz listy myślnikowe."""
    if not tekst.startswith('---'):
        return {}, tekst
    czesci = tekst.split('---', 2)
    if len(czesci) < 3:
        return {}, tekst
    blok, tresc = czesci[1], czesci[2]
    meta, biezacy_klucz = {}, None
    for linia in blok.splitlines():
        if not linia.strip():
            continue
        if re.match(r'^\s*-\s+', linia):
            if biezacy_klucz:
                meta.setdefault(biezacy_klucz, [])
                if isinstance(meta[biezacy_klucz], list):
                    meta[biezacy_klucz].append(linia.split('-', 1)[1].strip())
        elif ':' in linia:
            k, v = linia.split(':', 1)
            k, v = k.strip(), v.strip()
            biezacy_klucz = k
            meta[k] = v if v else []
    return meta, tresc

def parsuj_plik(sciezka):
    with open(sciezka, encoding='utf-8') as plik:
        tekst = plik.read()
    meta, tresc = _parse_frontmatter(tekst)
    fname = os.path.basename(sciezka)
    m = ID_RE.match(meta.get('id','') or fname)
    ident = (meta.get('id') or (m.group(1) if m else fname)).strip()
    wezel = {
        'id': ident,
        'typ': meta.get('typ', 'nieokreślony'),
        'tytul': meta.get('tytul', '').strip(),
        'status_epistemiczny': meta.get('status_epistemiczny', 'zweryfikowane'),
        'wersja': str(meta.get('wersja', '')).strip(),
        'zrodla': meta.get('zrodla', []) if isinstance(meta.get('zrodla'), list) else [],
        'sciezka': sciezka,
    }
    odw = meta.get('odwolania', [])
    krawedzie = [(ident, cel, 'odwoluje_sie_do') for cel in (odw if isinstance(odw, list) else [])]
    return wezel, krawedzie

def zbuduj_indeks(katalog_kanonu, indeks):
    """Buduje indeks z WYŁĄCZNIE kanonu. Odtwarzalne od zera."""
    indeks.rebuild()
    pliki = sorted(glob.glob(os.path.join(katalog_kanonu, '**', '*.md'), recursive=True))
    wszystkie_krawedzie = []
    n = 0
    for p in pliki:
        wezel, krawedzie = parsuj_plik(p)
        indeks.dodaj_wezel(wezel)
        wszystkie_krawedzie += krawedzie
        n += 1
    for zr, cel, typ in wszystkie_krawedzie:
        indeks.dodaj_krawedz(zr, cel, typ)
    return n
