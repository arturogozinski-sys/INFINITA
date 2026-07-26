# INFINITA

Repozytorium łączy kanon wiedzy, jego warsztat oraz rdzeń techniczny służący do parsowania, indeksowania i kontroli integralności.

## Co ma jaki status

- `kanon/` — aktywne źródło prawdy treściowej. Plik w tym katalogu musi mieć status produkcyjny `kanon` i epistemiczny `zweryfikowane`.
- `00_FUNDAMENT/` — reguły projektu, rejestry kontroli i raporty przekrojowe. Nie jest workiem na nowe treści kanoniczne.
- `robocze/` — warsztat, kandydaci, hipotezy, eksperymenty i wyniki prób. Materiał stąd nie staje się kanonem przez samo użycie albo poprawny test.
- `fikstury_demo/` — dane demonstracyjne rdzenia. Sprawdzają kod, nie prawdziwość ani kompletność kanonu.
- `rdzen/`, `narzedzia/`, `tests/` — mechanika wykonawcza i jej kontrole.

„Prototyp” opisuje dojrzałość mechaniki technicznej, nie status dokumentu. Statusy dokumentów określają pola zapisane w materiale i reguły `kanon/S002.md`.

## Źródła wykonawcze

- treść kanoniczna: `kanon/`,
- kontrakt danych i jego jedyna wersja: `schemat_grafu.json`,
- opis kontraktu dla człowieka: `SCHEMAT_GRAFU_INFINITA.md`,
- zasady pracy: `00_FUNDAMENT/`,
- kontrakt przekazania: `przekazania/HANDOFF_TEMPLATE.yaml`.

## Pełna kontrola lokalna

```text
python -m unittest discover -s tests -p "test_*.py" -v
python narzedzia/zbuduj_kanon.py
python narzedzia/audyt_semantyczny.py
python narzedzia/generuj_raport_martwych_odwolan.py --check
python narzedzia/waliduj_handoff.py przekazania/HANDOFF_TEMPLATE.yaml --template
```

Testy mają być bez efektów ubocznych w śledzonych plikach. Snapshot transportowy jest budowany wyłącznie z obiektów wskazanego commita, więc zawartość niezapisana w Git nie może wejść do pakietu podpisanego jego SHA.
