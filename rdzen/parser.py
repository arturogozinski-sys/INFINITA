# -*- coding: utf-8 -*-
"""Parser kanonu (Proces produkcji wiedzy: PARSER czyta WYŁĄCZNIE kanon).
Markdown + front-matter YAML -> węzły + krawędzie -> indeks (przez warstwę abstrakcji).
Parser nie zna silnika bazy — dostaje obiekt RepozytoriumIndeksu.
Bez zależności zewnętrznych: minimalny parser YAML front-matter (klucz: wartość + listy).

Budowa indeksu jest jedną obowiązkową operacją, nie luźnym łańcuchem kroków:
parse_all -> validate_all -> validate_graph -> transactional_replace.
Baza jest dotykana WYŁĄCZNIE gdy cały zbiór przejdzie walidację (patrz zbuduj_indeks).
"""
import os, re, glob
from rdzen.walidator import Walidator

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
        if re.match(r'^\s*-\s+', linia):  # element listy
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
    # krawędzie z pola 'odwolania' (lista identyfikatorów)
    odw = meta.get('odwolania', [])
    krawedzie = [(ident, cel, 'odwoluje_sie_do') for cel in (odw if isinstance(odw, list) else [])]
    return wezel, krawedzie

class BledyWalidacji(Exception):
    """Zbiorczy błąd fazy walidacji (schemat lub integralność grafu).
    Jeśli to leci, baza NIE została dotknięta — poprzedni stan pozostaje nienaruszony."""
    def __init__(self, naruszenia):
        self.naruszenia = list(naruszenia)
        super().__init__("\n".join(self.naruszenia))


def parse_all(katalog_kanonu):
    """Faza 1: sparsuj wszystkie pliki .md w katalogu. Nic nie zapisuje do bazy."""
    pliki = sorted(glob.glob(os.path.join(katalog_kanonu, '**', '*.md'), recursive=True))
    wezly, krawedzie = [], []
    for p in pliki:
        wezel, kraw = parsuj_plik(p)
        wezly.append(wezel)
        krawedzie += kraw
    return wezly, krawedzie


def validate_all(wezly, walidator: Walidator):
    """Faza 2: Walidator.sprawdz_wezel na KAŻDYM węźle. Zwraca listę wszystkich naruszeń."""
    naruszenia = []
    for w in wezly:
        naruszenia += walidator.sprawdz_wezel(w)
    return naruszenia


def validate_graph(wezly):
    """Faza 3: integralność zebranego zbioru przed zapisem — duplikaty ID między plikami."""
    naruszenia = []
    pliki_wg_id = {}
    for w in wezly:
        pliki_wg_id.setdefault(w['id'], []).append(w['sciezka'])
    for ident, pliki in sorted(pliki_wg_id.items()):
        if len(pliki) > 1:
            naruszenia.append(f"{ident}: zduplikowany identyfikator w plikach: {', '.join(pliki)}")
    return naruszenia


def transactional_replace(indeks, wezly, krawedzie, wersja_schematu):
    """Faza 4: rebuild() + zapis wszystkiego. Wywoływana WYŁĄCZNIE po przejściu walidacji.
    wersja_schematu pochodzi z schemat_grafu.json (Walidator.wersja_schematu) — jedyne źródło."""
    indeks.rebuild()
    indeks.ustaw_wersje_schematu(wersja_schematu)
    for w in wezly:
        indeks.dodaj_wezel(w)
    for zr, cel, typ in krawedzie:
        indeks.dodaj_krawedz(zr, cel, typ)
    return len(wezly)


def zbuduj_indeks(katalog_kanonu, indeks, sciezka_schematu=None):
    """Buduje indeks z WYŁĄCZNIE kanonu. Odtwarzalne od zera (Konstytucja, sekcja II).
    Obowiązkowy przepływ: parse_all -> validate_all -> validate_graph -> transactional_replace.
    Rzuca BledyWalidacji i NIE dotyka bazy, jeśli którykolwiek węzeł narusza schemat
    albo zbiór zawiera zduplikowane identyfikatory."""
    if sciezka_schematu is None:
        sciezka_schematu = os.path.join(os.path.dirname(__file__), '..', 'schemat_grafu.json')
    walidator = Walidator(sciezka_schematu)

    wezly, krawedzie = parse_all(katalog_kanonu)

    naruszenia = validate_all(wezly, walidator)
    if naruszenia:
        raise BledyWalidacji(naruszenia)

    naruszenia = validate_graph(wezly)
    if naruszenia:
        raise BledyWalidacji(naruszenia)

    return transactional_replace(indeks, wezly, krawedzie, walidator.wersja_schematu)
