# REJESTR REGULATORÓW — PILOTAŻ

Status: pilotaż  
Miejsce: `00_FUNDAMENT/REJESTR_REGULATOROW.md`  
Zakres: regulacje współpracy operatora, GPT i Claude’a  
Pozycja: poza grafem kanonu

## 1. Funkcja

Rejestr jest indeksem regulatorów, nie źródłem ich treści.

Źródłem reguły pozostaje dokument wskazany w kolumnie `Źródło`. Rejestr przechowuje wyłącznie informacje przekrojowe potrzebne do egzekwowania, testowania i przeglądu reguł.

Pilotaż obejmuje siedem regulatorów, które zawiodły albo zostały bezpośrednio ujawnione podczas sesji roboczej. Nie rozszerza się go przed oceną, czy tabela działa bez domysłów i zbędnej biurokracji.

## 2. Warstwy

- **A — regulacje zespołu:** określają, co obowiązuje w pracy operatora i modeli.
- **B — kanon merytoryczny:** dostarcza modeli i podstaw wyjaśniających; nie zmienia automatycznie regulacji zespołu.
- **C — egzekwowanie i pomiar:** testy, CI, bramki, raporty i przeglądy realizujące decyzje z warstwy A.

Poziom egzekwowania jest decyzją regulacyjną. Kod i CI wykonują poziom zapisany w rejestrze, lecz nie ustanawiają go samodzielnie.

## 3. Poziomy egzekwowania

- **L0 — wskazówka:** naruszenie pogarsza formę lub styl, ale nie zmienia podstawy decyzji ani integralności systemu.
- **L1 — obowiązek ujawnienia albo korekty:** naruszenie tworzy koszt, niejasność lub dodatkową pracę, lecz pozostaje łatwo wykrywalne i odwracalne.
- **L2 — zatrzymanie działania:** naruszenie prowadzi do pracy na złej podstawie, pracy niezamówionej albo utraty przejmowalności.
- **L3 — blokada zapisu, merge’a albo skutku zewnętrznego:** naruszenie zagraża integralności wspólnego źródła, dopuszcza niedozwolony stan lub wywołuje istotny skutek zewnętrzny.

## 4. Role domyślne

Jeżeli rejestr nie wskazuje odstępstwa:

- właściciel decyzji: operator,
- wykonawca: model realizujący zadanie,
- egzekwowanie: CI, jeżeli reguła jest automatyzowalna; w pozostałych przypadkach model,
- przegląd: operator,
- zgłaszający naruszenie techniczne: automat,
- zgłaszający naruszenie pracy modelu: sprawca, drugi model albo operator.

W rejestrze wpisuje się role tylko wtedy, gdy odbiegają od tych wartości.

## 5. Próba naruszenia i skuteczność

- **Próba naruszenia** sprawdza, czy mechanizm egzekwowania działa technicznie.
- **Wskaźnik skuteczności** sprawdza, czy regulator zmniejsza problem, dla którego powstał.

Sposób rozpoznania działania reguły określa się przy jej tworzeniu, nie dopiero po poznaniu wyniku. Pole niemierzalne pozostaje `nieustalone`; nie jest uzupełniane domysłem.

## 6. Rejestr pilotażowy

| ID | Reguła | Źródło | L | Podstawa kanoniczna | Egzekwowanie | Próba naruszenia | Skutek naruszenia | Stan | Wskaźnik skuteczności |
|---|---|---|---:|---|---|---|---|---|---|
| W01 | Żaden uczestnik nie rozpoczyna pracy na stanie, którego nie potwierdził. Brak potwierdzenia oznacza zatrzymanie, nie domysł. | `ZASADY_WSPOLPRACY.md`, zasada 2 | L2 | do ustalenia | bramka commita i jawne potwierdzenie wejścia | nieistniejący albo niezgodny SHA | zatrzymanie przed analizą lub produkcją | zapisana / wykonywana / częściowo mierzona | liczba przypadków pracy rozpoczętej na błędnym stanie |
| W02 | Czasownik operatora rozstrzyga tryb: `oceń`, `sprawdź`, `zaproponuj` nie tworzą plików; `zrób`, `napisz`, `wygeneruj` uruchamiają produkcję. | `ZASADY_WSPOLPRACY.md`, protokół 6 | L2 | do ustalenia | model przed rozpoczęciem zadania | polecenie `oceń` powoduje utworzenie lub zmianę pliku | zatrzymanie produkcji i zgłoszenie naruszenia | zapisana / wykonywana | liczba przypadków niezamówionej produkcji |
| W03 | Działanie kosztowne, nieodwracalne albo istotnie zmieniające projekt wymaga dwóch potwierdzeń `1`. | `ZASADY_WSPOLPRACY.md`, protokół 5 | L2 lub L3 zależnie od skutku | do ustalenia | model i mechanizm zapisu | pojedyncze `1` przy operacji wymagającej dwóch potwierdzeń | brak wykonania; przy skutku zewnętrznym blokada | zapisana / wykonywana | liczba operacji wykonanych bez wymaganego drugiego potwierdzenia |
| W04 | Model nie twierdzi, że stan został zmieniony, zapisany, scalony, przetestowany albo wdrożony bez potwierdzenia po wykonaniu. Dozwolone stany raportowania: `zweryfikowane`, `niezweryfikowane`, `sprzeczne z wcześniejszym twierdzeniem`. | ustalenie robocze R1; wymaga wpisania do dokumentu źródłowego | L2 | zasada uczciwości epistemicznej — do wskazania | kontrola wyniku przez narzędzie lub ponowny odczyt | raport `zrobione` bez odczytu stanu docelowego | korekta raportu, jawne oznaczenie stanu i zatrzymanie dalszych zależnych działań | uzgodniona / jeszcze niezapisana w źródle | liczba korekt twierdzeń o wykonanym stanie |
| W05 | Model nie przerzuca na operatora nieuzgodnionego ręcznego transportu artefaktu, jeżeli dostępny uczestnik albo narzędzie może umieścić go bezpośrednio. Jeżeli transport jest nieunikniony, wymaga uzgodnienia przed produkcją. | ustalenie robocze R2; wymaga wpisania do dokumentu źródłowego | L1 | zasada zero | model planujący produkcję | przygotowanie artefaktu wymagającego pobrania i ręcznego przeniesienia mimo dostępnego zapisu bezpośredniego | korekta ścieżki dostarczenia albo uzgodnienie ręcznego transportu | uzgodniona / jeszcze niezapisana w źródle | liczba ręcznych przekazań narzuconych operatorowi |
| W06 | Model nie produkuje kolejnej pełnej wersji tego samego artefaktu bez jednoznacznego sygnału zastąpienia, wariantu albo korekty poprzedniej wersji. | ustalenie robocze R3; wymaga wpisania do dokumentu źródłowego | L1 | minimalizacja kosztu i jednego aktywnego źródła funkcji — do wskazania | model przed utworzeniem kolejnej wersji | druga pełna wersja bez `0`, `skróć`, `popraw`, `wariant` albo równoważnej komendy | zatrzymanie i wskazanie istniejącej wersji | uzgodniona / jeszcze niezapisana w źródle | liczba niezamówionych równoległych wersji |
| W07 | Wynik modelu musi być przejmowalny. Kończąc pracę, model pozostawia minimalny stan pozwalający drugiemu uczestnikowi ją kontynuować bez własnego powrotu. | `ZASADY_WSPOLPRACY.md`, zasada 3; rozwinięcie R4 | L2 | do ustalenia | model kończący etap | wynik wymaga powrotu tego samego modelu albo nie wskazuje stanu, ograniczeń i następnego kroku | zatrzymanie zamknięcia zadania i uzupełnienie przekazania | zapisana / wykonywana | liczba zadań zablokowanych przez brak przejmowalnego stanu |

## 7. Ograniczenia pilotażu

1. Rejestr nie zmienia treści `ZASADY_WSPOLPRACY.md`.
2. Reguły W04–W06 są uzgodnione, lecz nie mają jeszcze zapisu źródłowego; rejestr oznacza ten brak zamiast udawać, że zapis istnieje.
3. Pilotaż nie rozstrzyga jeszcze pełnej symetrii obowiązków operatora i modeli. Symetria dotyczy uczciwości epistemicznej, lecz role i mechanizmy egzekwowania nie są identyczne.
4. Nie dodaje się teraz front matteru regulacjom ani generatora rejestru.
5. Nie mierzy się kosztu dojścia do decyzji, dopóki nie istnieje wiarygodny wskaźnik.
6. Nie scala się obecnie audytów i nie automatyzuje wygaszania ostrzeżeń.

## 8. Kryterium oceny pilotażu

Pilotaż jest użyteczny, jeżeli dla siedmiu reguł można bez domysłu ustalić:

- źródło,
- poziom egzekwowania,
- próbę naruszenia,
- skutek naruszenia,
- stan zapisania i wykonywania,
- mierzalny albo jawnie nieustalony wskaźnik skuteczności.

Jeżeli tabela wymaga wyjątków, dubluje treść źródłową albo tworzy więcej pracy niż usuwa, należy poprawić model rejestru przed dodaniem kolejnych regulatorów.
