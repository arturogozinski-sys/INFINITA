# INFINITA CORE — prototyp rdzenia (parser + indeks)

Wersja: 0.6 (linia: 0.5 -> 0.6 dodano walidator schematu + kontrakt danych SCHEMAT_GRAFU v1.0)

Dowód przepływu end-to-end: plik kanonu -> parser -> indeks -> zapytanie -> czujnik integralności.
Zgodny z Konstytucją Techniczną (warstwa abstrakcji, indeks pochodny) i Procesem Produkcji Wiedzy (parser czyta tylko kanon).

## WAŻNE: to jest prototyp, nie kanon
Pliki w `fikstury_demo/` (M044, M045) są DANYMI DEMONSTRACYJNYMI, status `demonstracyjne`.
NIE są kanonem repozytorium. Kod udowadnia przepływ; treść musi jeszcze przejść proces produkcji i recenzję właściciela, zanim stanie się kanonem.

## Struktura
- `rdzen/repozytorium.py` — warstwa abstrakcji indeksu (SQLite teraz, Postgres = inna klasa, ten sam kontrakt). Indeks pochodny, odtwarzalny.
- `rdzen/parser.py` — Markdown + YAML front-matter -> węzły + krawędzie. Czyta wyłącznie kanon.
- `fikstury_demo/` — dane demonstracyjne (NIE kanon).
- `tests/test_core.py` — formalny test (unittest/pytest, wykrywany przez CI).
- `tests/test_e2e.py` — skrypt poglądowy z wypisem.
- `.github/workflows/ci.yml` — CI uruchamia testy na każdy push.

## Uruchomienie
    python -m unittest discover -s tests -p "test_*.py" -v   # formalne, jak w CI
    python tests/test_e2e.py                                  # poglądowe z wypisem

## Raport testu (2026-07-21, v0.3)
5 testów, wszystkie OK przez unittest:
- węzeł przechodzi całą drogę (status = demonstracyjne, nie kanon),
- krawędzie grafu powstają,
- czujnik martwych krawędzi wykrywa nieistniejące odwołania,
- indeks odtwarzalny (przebudowa daje identyczny wynik),
- wersja schematu zapisana w indeksie.

## Naprawione w v0.5
- Komunikat diagnostyczny mówił „z N plików kanonu”, choć czyta fikstury_demo. Zmieniono na „pliki wejściowe (fikstury demonstracyjne)” — ostatni ślad starego nazewnictwa usunięty, żeby napis nie sugerował kanonu.

## Naprawione w v0.4
- Wyciek połączenia SQLite (unclosed database). Dodano close(), context manager i __del__ w IndeksSQLite; testy zamykają przez addCleanup. Zweryfikowane PEŁNYM `discover -W error::ResourceWarning` (nie zawężonym do jednego pliku).
- Kontrakt RepozytoriumIndeksu wymaga teraz close() — każdy silnik musi go zaimplementować.

## Naprawione w v0.3
- Wyciek uchwytu pliku w parserze (open bez zamknięcia) -> context manager. Zweryfikowane: testy przechodzą pod `-W error::ResourceWarning`.

## Dług techniczny (świadomy)
- Parser YAML jest minimalny (klucz:wartość + listy). Przy bogatszych metadanych rozważyć pyyaml.
- Walidacja schematu wejdzie po powstaniu SCHEMAT_GRAFU.md (typy węzłów/krawędzi są teraz dowolne).
