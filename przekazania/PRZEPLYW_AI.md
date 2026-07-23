# PRZEPŁYW PRACY AI W INFINITA

## Cel

Utrzymać jedno źródło prawdy, ograniczyć ręczne przenoszenie kontekstu i umożliwić niezależną kontrolę pracy modeli.

## Jedno źródło prawdy

Repozytorium GitHub `arturogozinski-sys/INFINITA` jest trwałym i wersjonowanym miejscem pracy.

- `master` zawiera stan przyjęty.
- Krótkie gałęzie robocze zawierają propozycje zmian.
- Pull request jest miejscem testów, dyskusji i recenzji.
- ZIP jest wyłącznie nośnikiem transportowym i nie stanowi źródła prawdy.

## Role

### Operator

- wyznacza kierunek,
- zatwierdza zakres i decyzje merytoryczne,
- dopuszcza zmianę do `master`.

### GPT

- pomaga planować i priorytetyzować,
- porównuje wyniki z celem i dokumentami nadrzędnymi,
- recenzuje raporty i rozstrzyga z operatorem dalszą drogę.

### Claude

- wykonuje cięższe audyty, symulacje i większe pakiety zmian,
- pracuje na stanie wskazanym pełnym SHA,
- oddaje wynik wraz z `HANDOFF.yaml` i raportem.

### GitHub Copilot

- działa przy aktualnym repozytorium,
- uruchamia testy i analizuje diff,
- robi code review,
- przygotowuje małe poprawki techniczne,
- nie zatwierdza samodzielnie własnej pracy.

## Podstawowy cykl zmiany

1. Operator określa jedno zadanie i kryterium zakończenia.
2. Wykonawca pracuje na wskazanym commicie bazowym.
3. Zmiany trafiają na krótką gałąź roboczą.
4. CI uruchamia testy i kontrole integralności.
5. Copilot analizuje diff i wyniki CI.
6. GPT i operator oceniają sens, zgodność i ryzyko.
7. Po akceptacji PR jest scalany do `master`.
8. `STAN_AKTUALNY.md` jest aktualizowany tylko wtedy, gdy zmienił się punkt wejścia projektu.

## Przekazanie materiału Claude’a

Każde przekazanie musi zawierać:

- `HANDOFF.yaml`,
- dokładny commit bazowy,
- opis celu i zakresu,
- wynik jako patch, snapshot lub raport,
- listę zmienionych plików,
- wykonane testy i ich wynik,
- ograniczenia i decyzje pozostawione operatorowi.

Raporty techniczne trafiają do:

`audyty/claude/YYYY-MM-DD_nazwa-zadania/`

Nie trafiają do `kanon/`, chyba że operator przeprowadzi osobny proces produkcji wiedzy.

## Zasady dla ZIP

- Nie commitujemy ZIP obok rozpakowanej zawartości.
- ZIP po imporcie może zostać zachowany poza repo jako kopia transportowa.
- Snapshot nie może zastąpić nowszego stanu repo bez porównania z `commit_bazowy`.
- Brak zgodności commita bazowego zatrzymuje automatyczny import.

## Klasy zadań

Każde zadanie otrzymuje jeden tryb:

- `implementacja`,
- `audyt`,
- `symulacja`,
- `synteza`,
- `redakcja`,
- `diagnoza`.

Nie łączymy pełnego audytu repo z implementacją drobnej poprawki w jednym przebiegu, chyba że zakres jawnie tego wymaga.

## Kryterium zakończenia

Zadanie jest zakończone, gdy:

- uzgodniony rezultat istnieje,
- odpowiednie testy przeszły,
- CI nie zgłasza błędu,
- drzewo robocze pozostaje czyste,
- raport wskazuje niepewności,
- niezależny recenzent zaakceptował zmianę.

## Automatyzacja etapami

### Etap 1 — kontrolowany

Import materiałów jest wykonywany przez GPT lub człowieka. Narzędzie przygotowuje diff i testy, ale nie scala zmian automatycznie.

### Etap 2 — półautomatyczny

Skrypt importu tworzy gałąź i draft PR po potwierdzeniu commita bazowego oraz przejściu testów.

### Etap 3 — automatyczny technicznie

Copilot może realizować małe, dobrze określone issues. Scalanie nadal wymaga niezależnej recenzji.

Automatyzacja nie obejmuje samodzielnej zmiany kanonu ani dokumentów najwyższej rangi.
