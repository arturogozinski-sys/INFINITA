# Nadzór nad INFINITA

INFINITA przyjmuje pomysły i wkład z zewnątrz, ale zachowuje jednoznaczną
odpowiedzialność za kierunek. Otwartość oznacza dostęp do rozmowy i możliwość
wniesienia wkładu. Nie oznacza współwłasności marki, automatycznego wpływu na
roadmapę ani prawa do scalenia zmiany.

## Role

### Właściciel i Operator

Aktualnym właścicielem i Operatorem jest `@arturogozinski-sys`.

Operator:

- ustala kierunek, granice publicznej warstwy i kolejność prac;
- podejmuje ostateczne decyzje o przyjęciu, odrzuceniu i publikacji zmian;
- kontroluje `master`, `CODEOWNERS`, markę oraz dostęp do repozytorium;
- nadaje, ogranicza i odbiera pozostałe role;
- może zatrzymać zmianę z powodu ryzyka, braku danych albo niezgodności z
  kierunkiem, nawet gdy CI jest zielone.

### Opiekun

Opiekun działa w jawnie powierzonym obszarze i czasie. Może porządkować
zgłoszenia, przygotowywać zmiany i prowadzić przegląd techniczny. Nie zmienia
samodzielnie kierunku projektu, granicy publiczne–prywatne, zasad prawnych ani
statusu kanonu.

### Kontrybutor

Kontrybutor zgłasza pomysł, dokumentację, test lub kod zgodnie z
`CONTRIBUTING.md`. Wysłanie wkładu nie tworzy obietnicy jego przyjęcia ani
stałej roli w projekcie.

### Recenzent

Recenzent sprawdza wskazany zakres: zgodność z celem, dowody, testy, ryzyko,
prywatność albo jakość techniczną. Opinia recenzenta jest udokumentowanym
wkładem do decyzji. Prawo do scalenia pozostaje przy Operatorze, o ile nie
zostanie jawnie delegowane.

## Zasady nadawania ról

- Rola jest jawna, ograniczona zakresem i może być czasowa.
- Dostęp techniczny otrzymuje się według zasady najmniejszych uprawnień.
- Brak aktywności nie daje trwałego prawa do stanowiska ani decyzji.
- Role można łączyć, lecz osoba nie zatwierdza własnej zmiany jako niezależny
  recenzent.
- Zmiana właściciela, Operatora albo zasad sukcesji wymaga osobnej, jawnej
  decyzji poza zwykłym pull requestem.

## Przyjmowanie pomysłów

### 1. Zgłoszenie

Pomysł trafia do publicznego formularza GitHub. Zgłoszenie opisuje problem,
oczekiwany skutek, odbiorcę, granice i sposób sprawdzenia. Nie może zawierać
danych prywatnych, sekretów ani materiałów bez prawa do publikacji.

### 2. Wstępna kontrola

Operator albo opiekun sprawdza:

- zgodność z kierunkiem i publicznym zakresem INFINITA;
- powtórzenia oraz zależności od istniejących elementów;
- ryzyko prywatności, bezpieczeństwa, marki i praw osób trzecich;
- koszt wdrożenia i utrzymania;
- możliwość małego, sprawdzalnego eksperymentu.

Wynik kontroli to: `DO DOPRECYZOWANIA`, `KANDYDAT`, `ODRZUCONE` albo
`ARCHIWUM`. Uzasadnienie pozostaje przy zgłoszeniu.

### 3. Decyzja o eksperymencie

Status `KANDYDAT` pozwala przygotować eksperyment lub pull request. Nie oznacza
wpisania do roadmapy, kanonu ani publicznej obietnicy. Operator określa zakres,
warunek powodzenia i granicę przerwania pracy.

### 4. Realizacja i walidacja

Zmiana przechodzi osobną gałąź, pull request, CI i przegląd zgodnie z
`.github/REVIEW_POLICY.md`. Materiał demonstracyjny pozostaje oddzielony od
kanonu. Nowe twierdzenia zachowują jawne źródło i status poznawczy.

### 5. Rozstrzygnięcie

Operator wybiera jeden wynik:

- `PRZYJĘTE` — zmiana została scalona w nazwanym zakresie;
- `DO POPRAWY` — potrzebna jest konkretna korekta;
- `ODRZUCONE` — zmiana nie zostaje przyjęta;
- `ARCHIWUM` — materiał zostaje zachowany bez aktywnej realizacji.

Scalenie techniczne nie nadaje automatycznie statusu kanonicznego. Odrzucenie
pomysłu nie unieważnia jego autorstwa ani nie blokuje późniejszego powrotu.

## Granice kontroli

Żaden pomysł, głosowanie, liczba reakcji ani zewnętrzna popularność nie zmienia
automatycznie kierunku projektu. Operator nie może natomiast przypisać sobie
autorstwa cudzego wkładu ani użyć materiału poza jawnie ustalonymi warunkami.
Nierozstrzygnięte kwestie licencji i wkładu pozostają ograniczeniem opisanym w
`CONTRIBUTING.md`.

