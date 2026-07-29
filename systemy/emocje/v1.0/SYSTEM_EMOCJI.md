# SYSTEM EMOCJI INFINITA

## FUNKCJA I STATUS

Funkcja: roboczy dokument czystej treści logicznej modelu emocji.

Zakres: czternaście rodzin emocji, wspólny obieg, interfejs matryca–filtr, dekoder kategorialny, granice oraz otwarte połączenia.

Status konstrukcyjny: wejścia, operacje i wyjścia są przyjętą strukturą roboczą. Ich zgodność empiryczna pozostaje poza tym dokumentem i zostanie rozpatrzona po zamknięciu trzeciej warstwy modelu.

Dokument nie jest aktem kanonu, diagnozą, modelem klinicznym ani katalogiem wszystkich emocji.

## ARCHITEKTURA

Model zawiera dwa połączone kierunki opisu:

1. Matryca prowadzi od bodźca przez zmianę stanu, dynamikę, reakcję organizmu i działanie do skutku oraz nowego wejścia.
2. Filtr otrzymuje kategorialne ślady obiegu i wyznacza rodziny zgodne z tymi śladami.

Matryca opisuje przebieg. Filtr dekoduje opis. Filtr nie wyjaśnia przyczyny powstania emocji, nie symuluje dynamiki i nie odtwarza reakcji organizmu.

## RODZINY

Rodziny podstawowe:

- strach;
- złość;
- smutek;
- radość;
- wstręt;
- zaskoczenie.

Rodziny społeczne:

- wstyd;
- poczucie winy;
- zażenowanie;
- duma;
- wdzięczność;
- zawiść;
- zazdrość;
- pogarda.

Podział jest operacyjny. Lista nie jest uznana za pełną, granice rodzin za naturalne ani sygnatury rodzin za biologicznie niezmienne.

## WSPÓLNY OBIEG

### 1. Bodziec

Bodziec jest zmianą zewnętrzną albo wewnętrzną.

### 2. Nadanie znaczenia

Organizm odnosi zmianę do jednego lub wielu elementów:

- aktualnego stanu;
- potrzeb;
- celu;
- przewidywania;
- normy;
- własnego obrazu;
- pozycji;
- porównania;
- więzi;
- działania innej osoby.

### 3. Zmiana stanu

Ocena znaczenia organizuje czasowo:

- uwagę;
- pobudzenie;
- odczuwanie;
- gotowość do działania.

### 4. Dynamika

Dynamika zawiera:

- kierunek zmiany;
- szybkość narastania;
- natężenie;
- czas trwania;
- próg uruchomienia;
- podatność na sprzężenie zwrotne;
- sposób powrotu.

### 5. Reakcja organizmu

Reakcja obejmuje skoordynowane procesy:

- nerwowe;
- autonomiczne;
- hormonalne;
- metaboliczne;
- ruchowe.

Reakcja nie jest skutkiem jednej substancji.

### 6. Działanie

Działanie zmienia:

- sytuację;
- relację organizmu z sytuacją;
- model wewnętrzny sytuacji.

### 7. Skutek i sprzężenie zwrotne

Skutek działania oraz sygnały zewnętrzne i wewnętrzne stają się nowym wejściem.

Obieg wygasa, gdy nowe wejście osłabia warunki podtrzymujące stan. Obieg utrwala się, gdy nowe wejście je potwierdza.

## WYMIARY DEKODERA

Filtr przyjmuje dwanaście wymiarów wejściowych:

1. przedmiot oceny;
2. sprawstwo;
3. czas;
4. struktura relacji;
5. zgodność z przewidywaniem;
6. wpływ na cel, normę, integralność lub więź;
7. możliwość kontroli;
8. zakres przypisania;
9. ocena intencji;
10. stabilność oceny;
11. kierunek przygotowanego działania;
12. warunek domknięcia.

Każdy wymiar zawiera jedną lub kilka wartości określonych albo pojedynczą wartość nieokreśloną.

Wartość nieokreślona nie spełnia warunku koniecznego. Sama wartość nieokreślona nie odrzuca jednak kandydata na późniejszym etapie działania lub domknięcia.

## MAPA MATRYCA–FILTR

| Element przebiegu | Wymiar dekodera | Relacja logiczna |
| --- | --- | --- |
| Bodziec i jego znaczenie | Przedmiot oceny | wskazuje, czego dotyczy ocena |
| Bodziec i jego znaczenie | Sprawstwo | wskazuje przypisane źródło zdarzenia lub wyniku |
| Bodziec i jego znaczenie | Czas | rozróżnia zdarzenie aktualne, dokonane i przewidywane |
| Bodziec społeczny i jego znaczenie | Struktura relacji | rozróżnia porównanie, więź, interakcję i ekspozycję |
| Bodziec względem przewidywania | Zgodność z przewidywaniem | zachowuje zgodność, niezgodność albo brak aktywnego przewidywania |
| Znaczenie względem potrzeb, celów, norm, integralności i więzi | Wpływ | określa główne znaczenie używane do syntezy kandydatów |
| Ocena znaczenia i możliwego działania | Możliwość kontroli | rozróżnia możliwość zmiany, ograniczenie i brak wpływu |
| Ocena własnego ja, działania albo drugiej osoby | Zakres przypisania | rozróżnia pojedynczy czyn i całą osobę |
| Ocena działania innej osoby | Ocena intencji | zachowuje rozpoznaną intencję społeczną |
| Ocena drugiej osoby | Stabilność oceny | rozróżnia ocenę stałą, zmienną i nieokreśloną |
| Działanie | Kierunek przygotowanego działania | sprawdza zgodność kierunku ze zbiorem dopuszczalnym dla rodziny |
| Skutek, nowe wejście i wynik obiegu | Warunek domknięcia | sprawdza wygasanie, utrwalanie albo brak danych |
| Zmiana stanu | brak bezpośredniego wymiaru | połączenie otwarte |
| Parametry dynamiki | brak bezpośredniego wymiaru | połączenie otwarte |
| Reakcja organizmu | brak bezpośredniego wymiaru | połączenie otwarte |
| Warstwa fizyczna i chemiczna | brak bezpośredniego wymiaru | pomost założony, lecz niewykonany |

Mapowanie oznacza relację funkcjonalną, nie tożsamość matrycy z filtrem.

Brak bezpośredniego wymiaru oznacza, że obecny dekoder nie używa danego elementu. Nie oznacza, że element jest zbędny dla całego modelu.

## ALGORYTM FILTRA

### 1. Synteza kandydatów

Dla każdej rodziny sprawdzane są jej warunki konieczne.

Rodzina przechodzi do zbioru kandydatów, gdy każdy jej warunek konieczny ma część wspólną z odpowiednim wymiarem wejścia.

Filtr przewiduje także warunki wykluczające. W aktualnej strukturze żadna z czternastu rodzin nie używa aktywnego warunku wykluczającego.

### 2. Test działania

Kandydat pozostaje, gdy:

- obserwowany kierunek działania ma część wspólną z kierunkami dopuszczalnymi dla rodziny; albo
- kierunek działania jest nieokreślony.

### 3. Test domknięcia

Kandydat pozostaje, gdy:

- opisany mechanizm domknięcia jest zgodny z mechanizmem rodziny; albo
- domknięcie jest nieokreślone.

### 4. Wynik

- Jeden kandydat: nazwa rodziny.
- Brak kandydatów: nierozstrzygnięty brak pasującej rodziny.
- Więcej niż jeden kandydat: nierozstrzygnięty konflikt kandydatów.

Konflikt oznacza współzgodność wejścia z kilkoma regułami. Nie oznacza przejścia jednej emocji w drugą.

## GRANICE AKTUALNEJ STRUKTURY

Dekoder zaczyna pracę na wartościach kategorialnych. Nie zawiera jeszcze reguł tłumaczących narrację, zachowanie ani pomiar organizmu na te wartości.

Dekoder nie używa bezpośrednio:

- organizacji uwagi;
- poziomu pobudzenia;
- jakości odczuwania;
- parametrów dynamiki;
- procesów nerwowych;
- procesów autonomicznych;
- procesów hormonalnych;
- procesów metabolicznych;
- parametrów ruchowych;
- realizacji fizycznej i chemicznej.

Dekoder klasyfikuje stan wejściowy. Nie opisuje zależności ani przejść między rodzinami.

## OTWARTE POŁĄCZENIA

### Translacja materiału żywego

**Wejście:** nieustrukturyzowany opis, zachowanie albo pomiar.

**Oczekiwane wyjście:** wartości dwunastu wymiarów dekodera.

**Status:** niewypełnione.

### Dynamika

**Wejście:** zmiana stanu oraz parametry jej przebiegu.

**Oczekiwane wyjście:** trajektoria narastania, utrzymywania i wygaszania.

**Status:** struktura opisowa istnieje; wykonanie niewypełnione.

### Reakcja organizmu

**Wejście:** trajektoria stanu.

**Oczekiwane wyjście:** skoordynowana odpowiedź nerwowa, autonomiczna, hormonalna, metaboliczna i ruchowa.

**Status:** połączenie niewypełnione.

### Pomost fizyczny i chemiczny

**Założenie:** realizacja trajektorii podlega przepływowi, transportowi, przemianie, ograniczeniom energetycznym i czasowi reakcji.

**Oczekiwane wyjście:** operacyjny opis realizacji procesu.

**Status:** założone; niewykonane.

### Przejścia między rodzinami

**Wejście:** wynik obiegu i nowe wejście.

**Oczekiwane wyjście:** reguła utrzymania rodziny, jej wygaszenia albo przejścia do innej rodziny.

**Status:** niewypełnione.

### Zakres rodzin

**Wejście:** materiał wykraczający poza czternaście aktualnych rodzin.

**Oczekiwane wyjście:** zachowanie istniejącej rodziny, rozdzielenie jej albo utworzenie nowej jednostki.

**Status:** kryterium niewypełnione.

## STATUS TREŚCI

**Zbudowane:** wspólny obieg, czternaście rodzin, dwanaście wymiarów, mapa matryca–filtr, synteza kandydatów, test działania, test domknięcia oraz trzy rodzaje wyniku.

**Założone:** operacyjny podział rodzin i możliwość fizyczno-chemicznej realizacji trajektorii.

**Niewypełnione:** translacja materiału żywego, wykonanie dynamiki, połączenie z reakcją organizmu, operacjonalizacja warstwy fizyczno-chemicznej, przejścia między rodzinami oraz kryterium zakresu rodzin.

**Oczekuje na trzecią warstwę:** kontrola zgodności konstrukcji z materiałem rzeczywistym.

## MATERIAŁ POZA WARSTWĄ LOGICZNĄ

Testy, dowody, bibliografia, manifesty, historia procedur i odbiory pozostają w istniejących plikach oraz historii repozytorium. Nie stanowią treści tego dokumentu.