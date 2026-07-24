# PROTOKÓŁ RUCH → ODCZYT

## Cel

Zapewnić higienę pracy każdego automatu i wykonawcy poprzez rozdzielenie operacji zmieniającej stan od decyzji o kolejnym kroku.

## Zasada nadrzędna

Każda mutacja unieważnia wcześniejszy obraz stanu.

Po ruchu wykonawca nie przechodzi od razu do następnego ruchu. Najpierw odczytuje rezultat z właściwego źródła prawdy, porównuje go z oczekiwaniem i dopiero wtedy podejmuje kolejną decyzję.

Podstawowy rytm:

`odczyt → decyzja → jedna mutacja → odczyt wyniku → porównanie → następna decyzja`

## Jedna mutacja na krok

W jednym kroku wykonawczym należy wykonywać jedną logiczną mutację, chyba że operacja jest atomowa z definicji.

Nie wolno łączyć kilku zależnych zmian na podstawie założenia, że poprzednie zakończyły się sukcesem.

Przykłady mutacji:

- utworzenie lub aktualizacja pliku,
- utworzenie gałęzi,
- otwarcie lub zmiana PR,
- poproszenie o review,
- rozwiązanie wątku,
- uruchomienie workflow,
- publikacja artefaktu,
- scalenie,
- import materiału zewnętrznego.

## Obowiązkowy odczyt po ruchu

Po każdej mutacji wykonawca musi odczytać co najmniej:

1. czy operacja została przyjęta,
2. jaki obiekt faktycznie powstał lub się zmienił,
3. jaki jest jego aktualny identyfikator lub SHA,
4. czy wynik odpowiada oczekiwaniu,
5. czy pojawiły się nowe warunki, błędy lub konflikty.

Brak możliwości odczytu wyniku oznacza `STOP`, nie domniemany sukces.

## Źródła prawdy

Stan należy odczytywać z systemu, który faktycznie przechowuje wynik operacji:

- GitHub dla repozytorium, PR, review, CI, workflow i artefaktów,
- Google Drive dla plików i folderów Drive,
- plik `HANDOFF.yaml` dla przekazania materiału między modelami,
- pełny commit SHA dla stanu bazowego repozytorium,
- log lub status wykonania dla automatu technicznego.

Pamięć rozmowy, opis zamiaru i komunikat „request accepted” nie są źródłem końcowego stanu.

## Klasy ryzyka

### Niskie ryzyko

Odczyt może nastąpić po krótkiej serii niezależnych operacji tylko wtedy, gdy żadna z nich nie zależy od wyniku poprzedniej.

### Średnie ryzyko

Po każdej mutacji wymagany jest bezpośredni odczyt wyniku.

### Wysokie ryzyko

Przed mutacją i po niej wymagany jest świeży odczyt stanu, a operacja musi zawierać blokadę wersji, SHA, revision ID lub równoważny identyfikator.

Do wysokiego ryzyka należą w szczególności:

- scalenie PR,
- usunięcie lub nadpisanie pliku,
- import zmian na nowszy stan,
- zmiana dokumentu nadrzędnego,
- publikacja artefaktu jako nowej bazy pracy,
- operacja nieodwracalna albo trudna do cofnięcia.

## Warunek kolejnego kroku

Kolejny ruch jest dozwolony tylko wtedy, gdy:

- poprzedni wynik został odczytany,
- wynik odpowiada oczekiwaniu albo rozbieżność została jawnie obsłużona,
- aktualny stan jest znany,
- decyzja o następnym kroku wynika z aktualnego stanu, nie z planu sprzed mutacji.

W przeciwnym razie obowiązuje `STOP`.

## Raportowanie

Po każdym istotnym etapie wykonawca rozdziela:

- `STAN PRZED`,
- `RUCH`,
- `STAN PO`,
- `ROZBIEŻNOŚCI`,
- `NASTĘPNY DOZWOLONY KROK`.

Nie wolno raportować „zrobione”, dopóki `STAN PO` nie został potwierdzony.

## Zastosowanie do automatów

Każdy nowy workflow, skrypt lub agent powinien jawnie określać:

1. źródło stanu wejściowego,
2. identyfikator wersji wejścia,
3. pojedynczą mutację,
4. sposób odczytu wyniku,
5. warunki `STOP`,
6. warunek przejścia do następnego kroku,
7. sposób raportowania stanu końcowego.

Automat bez tych elementów jest niegotowy do pracy produkcyjnej.

## Relacja z innymi procedurami

Ten protokół jest zasadą ogólną.

`BRAMKA_PRZED_SCALENIEM.md` jest jego wyspecjalizowanym zastosowaniem dla pull requestów.

`MOST_CLAUDE.md` stosuje go przy eksporcie snapshotu, przekazaniu materiału i imporcie zmian Claude’a.

## Kryterium jakości

Wolniejszy proces z potwierdzonym stanem jest lepszy niż szybszy proces wymagający powtórzenia pracy po chaosie.

Nie optymalizujemy liczby ruchów. Optymalizujemy liczbę poprawnych, niepowtarzanych przebiegów.
