# BRAMKA PRZED SCALENIEM

## Cel

Nie dopuścić do scalenia pull requestu na podstawie nieaktualnego, niepełnego albo tylko domniemanego stanu.

## Zasada nadrzędna

Ta procedura jest wyspecjalizowanym zastosowaniem `PROTOKOL_RUCH_ODCZYT.md`.

Prośba o review nie jest review. Uruchomienie CI nie jest wynikiem CI. Brak widocznego błędu nie jest potwierdzeniem sukcesu.

Scalenie jest dozwolone wyłącznie po jawnej weryfikacji wszystkich warunków poniżej na aktualnym `head_sha` pull requestu.

## Obowiązkowe odświeżenie stanu

Po każdej operacji zmieniającej PR, gałąź, plik, review, wątek lub status CI wykonawca musi ponownie odczytać stan właściwego obiektu z GitHuba.

Dotyczy to w szczególności:

- dodania lub aktualizacji pliku,
- nowego commita,
- oznaczenia PR jako gotowego,
- poproszenia recenzenta,
- pojawienia się review,
- poprawienia uwagi,
- rozwiązania wątku,
- zakończenia CI,
- próby scalenia.

Nie wolno kontynuować na podstawie stanu sprzed ostatniej operacji.

## Warunki scalenia

Przed scaleniem muszą być jednocześnie spełnione wszystkie warunki:

1. PR jest otwarty i nie jest draftem.
2. Znany jest aktualny pełny `head_sha`.
3. CI i wymagane kontrole zakończyły się sukcesem albo jawnie stwierdzono, że dla tej zmiany nie występują.
4. Istnieje zakończone review niezależnego recenzenta.
5. Review dotyczy aktualnego `head_sha` albo zostało wykonane po ostatnim commicie.
6. Wszystkie uwagi blokujące zostały poprawione.
7. Wszystkie właściwe wątki review są rozwiązane.
8. Operator jawnie zatwierdził scalenie.
9. Bezpośrednio przed scaleniem ponownie odczytano stan PR, review, wątków i CI.
10. Operacja scalenia używa `expected_head_sha` równego właśnie odczytanemu `head_sha`.

Brak jednego warunku oznacza `STOP`. Wykonawca podaje brakujący warunek i nie scala.

## Zakazy bezwzględne

Nie wolno:

- scalać w tym samym przebiegu, w którym dopiero poproszono o review,
- uznawać pustej listy błędów za pozytywne review,
- uznawać `requested reviewer` za zakończone review,
- scalać po nowym commicie na podstawie starszej recenzji,
- scalać tylko dlatego, że GitHub technicznie oznacza PR jako `mergeable`,
- omijać bramki z powodu presji czasu, wygody albo przekonania, że zmiana jest mała,
- traktować własnej oceny wykonawcy jako niezależnej recenzji.

## Algorytm wykonawczy

1. Odczytaj aktualny PR i zapisz `head_sha`.
2. Odczytaj zakończone review.
3. Odczytaj nierozwiązane wątki.
4. Odczytaj CI i kontrole dla `head_sha`.
5. Sprawdź jawne zatwierdzenie operatora.
6. Zbuduj listę warunków `TAK/NIE/NIE DOTYCZY`.
7. Przy dowolnym `NIE` zatrzymaj proces.
8. Przy samych `TAK` i uzasadnionych `NIE DOTYCZY` ponownie odczytaj PR.
9. Jeżeli `head_sha` się zmienił, wróć do kroku 1.
10. Scal z `expected_head_sha`.
11. Po scaleniu odczytaj wynik i potwierdź faktyczny commit w `master`.

## Odświeżanie wiedzy w trakcie procesu

Wykonawca nie utrzymuje stanu procesu wyłącznie w pamięci rozmowy. Stan pochodzi każdorazowo z GitHuba.

Po każdej mutacji należy traktować wcześniejsze informacje jako potencjalnie nieaktualne. Raport końcowy musi rozdzielać:

- stan potwierdzony,
- działanie wykonane,
- wynik działania,
- warunki jeszcze niespełnione.

## Wyjątki

Wyjątek może zatwierdzić wyłącznie operator, jawnie i dla jednego wskazanego PR. Wyjątek nie może zastąpić kontroli `head_sha` ani potwierdzenia wyniku scalenia.
