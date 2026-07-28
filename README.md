# INFINITA

[![CI](https://github.com/arturogozinski-sys/INFINITA/actions/workflows/ci.yml/badge.svg)](https://github.com/arturogozinski-sys/INFINITA/actions/workflows/ci.yml)

INFINITA jest rozwijanym systemem budowania, porządkowania i sprawdzania wiedzy w postaci grafu. Łączy treść źródłową, jawny status poznawczy, walidację, indeks pochodny oraz modele wykonawcze, zachowując ludzką kontrolę nad kierunkiem i znaczeniem projektu.

Status: **aktywny prototyp badawczo-inżynieryjny**.

## Po co powstaje

Zwykłe repozytorium przechowuje pliki. INFINITA ma dodatkowo pilnować:

- skąd pochodzi twierdzenie;
- jaki ma status i poziom wiarygodności;
- z czym jest powiązane;
- czy przeszło wymagane kontrole;
- czy wynik można odtworzyć;
- czy zmiana nie zerwała wcześniejszych zależności.

Docelowo projekt ma umożliwiać współtworzenie wiedzy bez utraty jej pochodzenia, granic i odpowiedzialności za decyzje.

## Co działa obecnie

- schemat grafu `1.1` z typami węzłów, krawędzi i ograniczeniami;
- parser dokumentów Markdown z metadanymi YAML;
- walidator struktury i statusu epistemicznego;
- transakcyjnie przebudowywany indeks SQLite;
- czujniki duplikatów, martwych odwołań i niespójności semantycznych;
- bramka wejściowa i raport różnicowy dla zmian wprowadzanych przez modele;
- testy jednostkowe i audyt realnego katalogu `kanon/` w GitHub Actions;
- roboczy system emocji `1.0` z modelem maszynowym i projekcją wykonawczą.

## Granice

INFINITA nie jest systemem autonomicznie ustanawiającym prawdę. Kod sprawdza strukturę, kontrakty i odtwarzalność, ale nie zastępuje oceny znaczenia ani jakości źródeł.

System emocji jest modelem strukturalnym i warstwą roboczą. Nie stanowi potwierdzenia biologicznego, narzędzia medycznego ani diagnozy człowieka.

Materiały w `fikstury_demo/` są danymi demonstracyjnymi. Nie należą do kanonu i nie uzyskują takiego statusu przez samo przejście testów.

## Architektura

| Warstwa | Miejsce | Funkcja |
| --- | --- | --- |
| Zweryfikowana treść | `kanon/` | Dane dopuszczone do grafu produkcyjnego |
| Dane demonstracyjne | `fikstury_demo/` | Jawne próbki do testowania przepływu |
| Rdzeń wykonawczy | `rdzen/` | Parser, walidator, indeks i modele |
| Systemy robocze | `systemy/` | Wersjonowane modele dziedzinowe |
| Narzędzia | `narzedzia/` | Audyty, raporty i operacje repozytorium |
| Kontrola jakości | `tests/`, `.github/workflows/` | Testy, CI i bramki integralności |
| Materiały robocze | `robocze/` | Hipotezy i kandydaci przed walidacją |
| Archiwum | `archiwum/` | Materiały zachowane historycznie |

Podstawowy przepływ:

```text
źródło → metadane → walidacja → parser → graf → indeks → zapytanie → kontrola integralności
```

Indeks jest warstwą pochodną. Można go odtworzyć z treści źródłowej i schematu.

## Uruchomienie

Środowisko referencyjne CI: Python 3.12.

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python tests/test_e2e.py
```

Pierwsza komenda uruchamia testy jednostkowe. Druga pokazuje demonstracyjny przepływ parser → indeks → zapytanie.

## System emocji

Aktywną wersję wskazuje:

```text
systemy/emocje/AKTYWNA_WERSJA.json
```

Dokument nadrzędny:

```text
systemy/emocje/v1.0/SYSTEM_EMOCJI.md
```

Publiczne CI sprawdza kontrakt adaptera na sztucznej próbce demonstracyjnej. Nie ładuje i nie przedstawia jako publicznie zweryfikowanego prywatnego korpusu walidacyjnego.

## Kontrola jakości

Każdy push uruchamia:

- testy jednostkowe;
- walidację realnego katalogu `kanon/`;
- czujniki spójności semantycznej;
- raport kondycji kanonu;
- raport różnicowy dla zmian modeli.

Aktualny stan pokazuje plakietka CI na początku dokumentu.

## Współtworzenie

Projekt jest przygotowywany do otwartej współpracy. Kierunek, zakres publicznego rdzenia i przyjęcie zmian pozostają decyzją opiekuna projektu.

Założenia współpracy:

- propozycje muszą jasno nazywać problem i skutek;
- zmiany powinny być małe, sprawdzalne i odwracalne;
- dane demonstracyjne nie mogą udawać zweryfikowanej treści;
- zielone CI jest warunkiem koniecznym, ale nie oznacza automatycznego przyjęcia zmiany;
- wkład nie może ujawniać danych prywatnych ani treści osób trzecich bez podstawy.

Formalne `CONTRIBUTING.md`, role, zasady przeglądu i polityka bezpieczeństwa są częścią dalszej roadmapy.

## Roadmapa

- ustabilizowanie granicy między rdzeniem publicznym a materiałami prywatnymi;
- opisanie publicznych kontraktów i przykładów użycia;
- dodanie zasad współtworzenia, przeglądu i bezpieczeństwa;
- rozstrzygnięcie licencji kodu i dokumentacji;
- przygotowanie wersjonowanych wydań;
- rozwijanie kolejnych systemów dziedzinowych bez obniżania wymagań walidacyjnych.

## Licencja

Licencja projektu nie została jeszcze rozstrzygnięta. Jej wybór oraz osobne zasady dla kodu i dokumentacji są otwartymi decyzjami projektowymi.

Materiały pochodzące ze źródeł zewnętrznych i ich warunki są opisane w
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). Dokument ten nie nadaje
licencji pozostałej części projektu.
