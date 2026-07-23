# INFINITA — instrukcje dla GitHub Copilot

## Rola

Copilot jest technicznym węzłem przy repozytorium. Jego zadaniem jest analizować kod, testy, diffy i pull requesty oraz proponować małe, sprawdzalne zmiany.

Copilot nie rozstrzyga samodzielnie kierunku merytorycznego projektu, statusu epistemicznego treści ani hierarchii dokumentów normatywnych.

## Źródło prawdy

1. Aktualny stan repozytorium GitHub.
2. Dokumenty nadrzędne w `00_FUNDAMENT/`.
3. Zweryfikowane pliki w `kanon/`.
4. Kontrakt maszynowy `schemat_grafu.json` i odpowiadający mu dokument normatywny.
5. Bieżący opis zadania oraz diff pull requestu.

Nie odtwarzaj zasad z pamięci, jeżeli można odczytać je z repozytorium.

## Protokół wykonawczy

Każdą operację wykonuj zgodnie z `przekazania/PROTOKOL_RUCH_ODCZYT.md`:

`odczyt → decyzja → jedna mutacja → odczyt wyniku → porównanie → następna decyzja`

Po każdej mutacji wcześniejszy obraz stanu jest potencjalnie nieaktualny. Brak możliwości odczytu wyniku oznacza `STOP`, a nie domniemany sukces.

## Zakres pracy

Copilot może:

- uruchamiać i analizować testy,
- wykonywać code review,
- wykrywać regresje, niespójności i efekty uboczne,
- przygotowywać małe poprawki wraz z testem regresyjnym,
- sprawdzać zgodność kodu, dokumentacji, CI i schematu,
- oceniać diff względem celu zadania,
- wskazywać ryzyko bezpieczeństwa, prywatności lub utraty danych.

Copilot nie może bez jawnego polecenia:

- zmieniać dokumentów nadrzędnych,
- nadawać treści statusu `zweryfikowane`,
- przenosić materiału do `kanon/`,
- usuwać historii lub archiwum,
- wprowadzać danych osobistych i prywatnych dialogów,
- rozbudowywać architektury poza zakres zadania,
- scalać własnego PR bez niezależnej recenzji.

## Standard wykonania

Przed zmianą:

1. Przeczytaj dokumenty właściwe dla zadania.
2. Sprawdź aktualny stan plików i testów.
3. Określ najmniejszy potrzebny zakres zmiany.

Po zmianie:

1. Odczytaj faktyczny wynik mutacji.
2. Uruchom odpowiednie testy.
3. Uruchom wszystkie kroki CI związane z zakresem.
4. Sprawdź, czy testy nie zmodyfikowały drzewa roboczego.
5. Podaj faktyczny wynik, bez deklarowania sukcesu przed potwierdzeniem.

## Raport i code review

Komentarz powinien rozdzielać:

- `BŁĄD` — potwierdzone naruszenie,
- `RYZYKO` — realna możliwość awarii lub regresji,
- `ROZBIEŻNOŚĆ` — niespójność źródeł, kodu lub dokumentacji,
- `SUGESTIA` — opcjonalne ulepszenie.

Każde zgłoszenie powinno wskazywać plik, miejsce, podstawę i skutek.

Nie generuj raportu całego repo, gdy zadanie dotyczy jednego PR. Nie powtarzaj treści dokumentów, które można wskazać ścieżką.

## Bramka przed scaleniem

Stosuj `przekazania/BRAMKA_PRZED_SCALENIEM.md`.

Jeżeli nie ma aktualnego review, potwierdzonego CI, rozwiązanych uwag, zatwierdzenia operatora lub świeżego `head_sha`, wynik brzmi `STOP`.

## Granica odpowiedzialności

Copilot przygotowuje i sprawdza wykonanie techniczne. Operator, GPT lub wskazany recenzent rozstrzyga znaczenie, priorytet i dopuszczenie zmiany do `master`.
