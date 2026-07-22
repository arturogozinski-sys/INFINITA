# MANIFEST ZADANIA DLA MODELU

Ten dokument jest bramką wejściową. Model nie rozpoczyna analizy repozytorium,
dopóki pola obowiązkowe nie są wypełnione i zgodne z raportem różnicowym.

## 1. Punkt odniesienia

- Repozytorium: `arturogozinski-sys/INFINITA`
- Gałąź: `<GAŁĄŹ>`
- Commit bazowy: `<PEŁNY_SHA>`
- Commit docelowy / HEAD: `<PEŁNY_SHA>`
- Data wygenerowania manifestu: `<YYYY-MM-DD HH:MM TZ>`
- Raport kondycji: `RAPORT_KONDYCJI.md`
- Raport różnicowy: `RAPORT_ROZNICOWY.md`

## 2. Cel zadania

`<JEDNO ZDANIE: JAKI WYNIK MA POWSTAĆ>`

## 3. Zakres do przeczytania

Model czyta wyłącznie pliki wskazane poniżej albo w sekcji `DO PRZECZYTANIA`
raportu różnicowego.

1. `<PLIK LUB ZAKRES LINII>`
2. `<PLIK LUB ZAKRES LINII>`

### Zakres wyłączony

- pliki wymienione w sekcji `NIE trzeba czytać`,
- historia repozytorium poza wskazanym zakresem commitów,
- dokumenty niezwiązane bezpośrednio ani przez sąsiedztwo jednego kroku,
- ponowne projektowanie architektury poza celem zadania.

## 4. Budżet zasobów

- Maksymalna liczba czytanych plików: **10**
- Maksymalna liczba czytanych linii: **3000**
- Maksymalna liczba dodatkowych plików po rozpoczęciu: **2**, wyłącznie z uzasadnieniem
- Zakaz czytania całego repozytorium
- Zakaz powtarzania istniejącego audytu bez wskazania nowej hipotezy

Jeżeli zadanie nie mieści się w budżecie, model zatrzymuje analizę i zwraca
minimalny wniosek o zmianę zakresu. Nie rozszerza zakresu samodzielnie.

## 5. Bramka przed analizą

Przed wykonaniem zadania model potwierdza:

```text
Potwierdzony commit docelowy:
Potwierdzony commit bazowy:
Potwierdzone pliki:
Łączna liczba plików:
Szacowana liczba linii:
Elementy niezweryfikowane:
Decyzja bramki: TAK / NIE
```

`NIE` oznacza zakończenie bez analizy merytorycznej.

## 6. Format wyniku

Wynik rozdziela:

1. **Obserwacje** — bezpośrednio potwierdzone w podanych plikach.
2. **Wnioski** — wynikające z obserwacji.
3. **Hipotezy** — jawnie oznaczone i niewprowadzane jako fakty.
4. **Propozycje zmian** — z listą dokładnych plików.
5. **Ograniczenia** — czego nie sprawdzono.

Model nie wgrywa zmian, jeśli zlecenie nie zawiera jawnej zgody na zapis.

## 7. Rejestr kosztu

```yaml
model: <NAZWA>
commit: <PEŁNY_SHA>
pliki_przeczytane: <LICZBA>
linie_przeczytane: <LICZBA>
zuzycie_kontekstu: <PROCENT LUB NIEZNANE>
wynik_uzyteczny: pelny | czesciowy | nieuzyteczny
glowny_problem: <PUSTE LUB OPIS>
```

## 8. Kryterium zakończenia

Zadanie jest zakończone, gdy wynik odpowiada celowi w zadanym zakresie,
a raport zawiera ograniczenia i rejestr kosztu. Odkrywanie całego stanu repo
nie jest częścią zadania, ponieważ stan dostarczają raporty automatyczne.
