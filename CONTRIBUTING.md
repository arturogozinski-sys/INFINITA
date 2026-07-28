# Współtworzenie INFINITA

INFINITA jest otwarta na pytania, pomysły, testy, dokumentację i kod. Otwartość
na wkład nie oznacza automatycznego przyjęcia zmiany. Operator odpowiada za
kierunek projektu i podejmuje ostateczną decyzję o scaleniu.

## Zanim zaczniesz

1. Sprawdź istniejące zgłoszenia i pull requesty.
2. Dla większej zmiany najpierw otwórz zgłoszenie opisujące problem, oczekiwany
   skutek i granice rozwiązania.
3. Nie umieszczaj danych osobowych, materiałów prywatnych, sekretów, danych
   dostępowych ani treści osób trzecich bez prawa do ich użycia.
4. Nie przedstawiaj hipotezy, demonstracji ani wyniku modelu jako
   zweryfikowanego faktu.

## Przygotowanie zmiany

- Pracuj na osobnej gałęzi.
- Utrzymuj jeden cel na pull request.
- Dodaj lub popraw testy, jeżeli zmieniasz zachowanie systemu.
- Wyjaśnij: co zmieniasz, dlaczego, jaki jest skutek i jak to sprawdzono.
- Zachowaj rozdział między `kanon/`, `fikstury_demo/`, `robocze/` i `archiwum/`.
- Przed wysłaniem uruchom:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python narzedzia/zbuduj_kanon.py
python narzedzia/audyt_semantyczny.py
```

## Przegląd i scalenie

Każda zmiana głównej gałęzi przechodzi przez pull request i zielone CI. Zmiana
osoby spoza właścicieli kodu wymaga decyzji Operatora. Wszystkie rozmowy
przeglądu muszą zostać rozwiązane, a gałąź zaktualizowana względem `master`.
Szczegóły znajdują się w `.github/REVIEW_POLICY.md`.

Zielone CI potwierdza spełnienie automatycznych kontroli. Nie potwierdza
poprawności znaczenia i nie gwarantuje przyjęcia wkładu.

## Stan zasad prawnych

Licencja kodu, licencja dokumentacji i warunki przyjmowania praw do wkładu są
jeszcze ustalane. Do czasu ich rozstrzygnięcia można zgłaszać pomysły i pull
requesty, ale zewnętrzny wkład może pozostać niescalony. Autor wkładu musi mieć
prawa do przekazywanego materiału. Samo wysłanie zmiany nie przenosi praw na
Operatora i nie oznacza zgody na inne warunki niż jawnie uzgodnione.

