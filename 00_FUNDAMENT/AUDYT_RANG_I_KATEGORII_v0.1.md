# Audyt rang i kategorii kanonu INFINITA v0.2

## Cel
Sprawdzić, czy dokumenty kanonu pełnią jedną rozpoznawalną funkcję, mają odpowiednią rangę i nie mieszają zasad, mechanizmów, procesów, specyfikacji oraz indeksów.

## Hierarchia rang
1. **Metakanon / konstytucja projektu** — `00_FUNDAMENT/`.
2. **Specyfikacje S** — określają reguły działania repozytorium i współpracy.
3. **Zasady Z** — nadrzędne regulatory decyzji obowiązujące w wielu domenach.
4. **Mechanizmy M** — opisują, jak i dlaczego zachodzi określone zjawisko.
5. **Procesy P** — opisują kolejność czynności, bramki i wyniki wykonawcze.
6. **Indeksy I** — definiują słowniki, mapy i etykiety; nie tworzą równoległych norm.
7. **Dowody E, przypadki C, dialogi D, hipotezy H** — materiały wspierające, ilustrujące lub oczekujące na walidację.

## Stan po drugim przebiegu

### Zasady
`Z006`, `Z007` i `Z008` pozostają trzema odrębnymi regulatorami:
- Z006 — priorytet trwałej sprawczości,
- Z008 — wybór drogi i zakresu zmiany,
- Z007 — kryterium integracji działania.

### P008 i I006
P008 został ukończony jako pełny proces dziesięciu kroków. Reguła redukcji i przydział stanów A–E znajdują się teraz w P008.

I006 jest wyłącznie indeksem etykiet: warstw, stanów obsługi, poziomów sterowania i flag. Nie podejmuje decyzji i nie zawiera równoległego protokołu.

### Rozdzielenie M045
Dawny dokument wielofunkcyjny został rozdzielony z zachowaniem funkcji:
- M045 — reguły jako regulatory przepływu oraz obejście kontra udrożnienie,
- M047 — minimalne tarcie, adaptacja do ram i planowanie drogi,
- S018 — współpraca człowiek–AI wobec reguł i ograniczeń.

M045 pozostawia jawną mapę podziału. Nowe dokumenty wskazują pochodzenie treści.

### Rozdzielenie M046
Dawny dokument wielofunkcyjny został rozdzielony na:
- M046 — stabilna adaptacja,
- M048 — stereoskopowa ocena decyzji i znaczenie czasu,
- P010 — antycypacyjne przygotowanie decyzji,
- M049 — walidacja przez analogie i poszukiwanie inwariantu.

M046 pozostawia jawną mapę podziału. M049 wyraźnie stwierdza, że analogia nie jest dowodem i nie może sama nadać statusu `zweryfikowane`.

### Pozostałe sygnały mieszania funkcji
- M003 zawiera sekwencję wykonawczą ekonomii poznawczej.
- M018 zawiera proces zarządzania budżetem poznawczym.
- M044 zawiera procedurę stabilizacji stanu.
- M049 zawiera procedurę badawczą wewnątrz mechanizmu; pozostaje to dopuszczalne tymczasowo, lecz czujnik powinien raportować sygnał.

Nie są to obecnie błędy unieważniające dokumenty. Następny przebieg powinien ocenić, czy procedury mają wystarczająco samodzielną funkcję, by utworzyć osobne dokumenty P.

## Czujniki
`narzedzia/audyt_semantyczny.py` sprawdza między innymi:
- zgodność nazwy pliku z identyfikatorem,
- zgodność jawnych relacji w treści z YAML,
- powrót starego modelu statusów,
- brak podstawowych sekcji dla danej rangi,
- procedury ukryte wewnątrz mechanizmów,
- dokumenty wielofunkcyjne,
- niedokończone procesy,
- normy ukryte w indeksach,
- martwe odwołania,
- regulatory bez relacji przychodzących.

Błędy obiektywne zatrzymują CI. Sygnały wymagające decyzji właściciela pozostają ostrzeżeniami.

## Następne prace
1. Ocenić wydzielenie procesów z M003, M018 i M044.
2. Zdefiniować jawne typy relacji: `wymaga`, `stosuje`, `ogranicza`, `uzupelnia`, `wynika_z`, `jest_w_napieciu_z`.
3. Rozstrzygnąć martwe odwołania i odwołania do materiałów roboczych.
4. Uruchomić audyt szczelności: usunięcie węzła, awaria relacji, konflikt statusu, regulator bez odbiorców oraz regresja kategorii.

## Werdykt
Po drugim przebiegu warstwy są wyraźniejsze: indeks nie normuje, proces wykonuje, mechanizm wyjaśnia, specyfikacja reguluje współpracę, a dokumenty syntetyczne pozostawiają ślad kontrolowanego podziału. System nadal wymaga testów szczelności i bogatszych relacji, lecz największe mieszanie rang zostało ograniczone bez utraty treści.