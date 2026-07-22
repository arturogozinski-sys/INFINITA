# Audyt rang i kategorii kanonu INFINITA v0.1

## Cel

Sprawdzić, czy dokumenty kanonu pełnią jedną rozpoznawalną funkcję, mają odpowiednią rangę i nie mieszają zasad, mechanizmów, procesów, specyfikacji oraz indeksów w jednym worku.

Audyt nie rozstrzyga automatycznie o usunięciu ani rozbiciu dokumentu. Dokument wielofunkcyjny jest najpierw oznaczany, a dopiero potem dzielony z zachowaniem pełnej treści i zależności.

## Proponowana hierarchia rang

1. **Metakanon / konstytucja projektu** — `00_FUNDAMENT/`.
2. **Specyfikacje S** — określają reguły działania repozytorium i procesu wiedzy.
3. **Zasady Z** — nadrzędne regulatory decyzji, obowiązujące w wielu domenach.
4. **Mechanizmy M** — opisują, jak i dlaczego zachodzi określone zjawisko.
5. **Procesy P** — opisują kolejność czynności i bramki wykonawcze.
6. **Indeksy I** — definiują słowniki, mapy i etykiety; nie powinny tworzyć równoległych reguł normatywnych.
7. **Dowody E, przypadki C, dialogi D, hipotezy H** — materiały wspierające, ilustrujące lub oczekujące na walidację.

## Ocena obecnego zestawu

### Specyfikacje

`S002`, `S003`, `S012`, `S016`, `S017` mają właściwą rangę specyfikacji. Są regulatorami repozytorium lub procesu pracy, a nie opisami pojedynczych mechanizmów.

Po korekcie S002 model dokumentu ma trzy niezależne wymiary: `typ`, `status_produkcyjny`, `status_epistemiczny`.

### Zasady

- `Z006` — regulator nadrzędny: trwała sprawczość przed wynikiem chwilowym.
- `Z008` — zasada decyzyjna podporządkowana Z006: wybór drogi i zakresu zmiany.
- `Z007` — zasada diagnostyczna: wykonanie nie dowodzi integracji.

Nie są duplikatami. Tworzą układ: priorytet nadrzędny → wybór działania → ocena kosztu integracji.

`Z007` leży blisko granicy między zasadą a mechanizmem, ale zachowuje rangę zasady, ponieważ ustanawia ogólne kryterium oceny, a nie opisuje wyłącznie przyczynowego przebiegu jednego zjawiska.

### Mechanizmy o poprawnie ograniczonej funkcji

- `M037` — przepustowość i wąskie gardła.
- `M039` — bufory, redundancja i margines bezpieczeństwa.
- `M040` — bezwładność, histereza i zależność od drogi.

Dokumenty te mają wyraźny przedmiot, opis przyczynowy i granice zastosowania.

### Mechanizmy zawierające fragment procesu

- `M003` zawiera pełną sekwencję postępowania w sekcji „Proces”. Rdzeń dokumentu jest mechanizmem/zasadą ekonomii poznawczej, lecz procedura może docelowo zostać wydzielona do dokumentu P.
- `M018` opisuje budżet poznawczy, ale również zawiera pięciostopniowy proces zarządzania nim.
- `M044` opisuje mechanizm stabilizacji i brak pogorszenia jako zysk, lecz zawiera sześciostopniową procedurę wykonawczą.

Nie są to obecnie błędy unieważniające dokumenty. Są to sygnały mieszania funkcji, które utrudnią późniejszą automatyzację i wyszukiwanie.

### Dokumenty wielofunkcyjne

#### M045

Łączy co najmniej pięć funkcji:

1. opis regulacji przepływu,
2. interpretację funkcji reguł i intencji regulatora,
3. zasadę minimalnego tarcia,
4. kryterium obejścia i udrożnienia,
5. normę współpracy człowiek–AI.

M045 jest wartościowym dokumentem syntetycznym, ale za szerokim jak na pojedynczy mechanizm. Nie należy go usuwać. Należy zachować jako źródło rozdzielenia i docelowo wydzielić z niego osobne węzły, pozostawiając jeden mechanizm główny oraz jawne relacje do zasad i procesu AI.

#### M046

Łączy:

1. stabilną adaptację,
2. ocenę stereoskopową,
3. czas jako składnik decyzji,
4. przygotowanie antycypacyjne,
5. warunki złożone i markery,
6. walidację przez analogie.

To co najmniej trzy odrębne mechanizmy. Dokument powinien zostać rozszczepiony dopiero po sporządzeniu mapy zależności, ponieważ obecna synteza może zawierać ważne połączenia między nimi.

### Proces P008

Ranga `proces` jest prawidłowa. Dokument deklaruje jednak dziesięć etapów, a rozwija tylko pierwsze trzy. Jest to niedokończony proces kanoniczny i najważniejsza luka funkcjonalna w obecnym zestawie.

Termin „status operacyjny” został zmieniony na „stan obsługi materiału”, aby nie mieszać routingu wejścia ze statusem produkcyjnym dokumentu.

### Indeks I006

Ranga `indeks` jest prawidłowa dla słownika warstw, stanów obsługi, sterowania i flag. Sekcja „Reguła redukcji” ma jednak charakter normatywny. Docelowo reguła powinna zostać przeniesiona do P008 albo specyfikacji, a I006 powinien pozostać słownikiem definicji.

## Naprawy wykonane w pierwszym przebiegu

1. Rozdzielono status dokumentu od stanu obsługi materiału w P008 i I006.
2. Ujednolicono jawne powiązania M045 w treści i YAML.
3. Dodano audyt semantyczny do CI.
4. Błędy obiektywne blokują CI, a sygnały kategorii i rangi są raportowane jako ostrzeżenia.

## Czujniki

`narzedzia/audyt_semantyczny.py` sprawdza:

- zgodność nazwy pliku z identyfikatorem,
- zgodność jawnej listy powiązań w treści z YAML,
- powrót niedookreślonego modelu `status operacyjny`, `OP-*`, `FN-*`,
- brak podstawowych sekcji wymaganych przez rangę dokumentu,
- procedury ukryte wewnątrz mechanizmów,
- dokumenty mechanizmów o nadmiernej liczbie sekcji,
- procesy deklarujące więcej kroków, niż faktycznie rozwijają,
- reguły normatywne ukryte w indeksach,
- martwe odwołania,
- zasady i specyfikacje bez odwołań przychodzących, czyli możliwe ważne regulatory zalegające na peryferiach grafu.

## Kolejność następnych prac

1. Uzupełnić P008 albo obniżyć jego status do kandydata do czasu ukończenia.
2. Przenieść regułę redukcji z I006 do P008 lub specyfikacji.
3. Sporządzić protokół rozszczepienia M045 i M046 bez utraty treści.
4. Wydzielić procedury z M003, M018 i M044 do warstwy P, pozostawiając w mechanizmach jedynie krótkie zastosowanie.
5. Zdefiniować jawne typy relacji, aby odróżnić `wymaga`, `stosuje`, `ogranicza`, `uzupełnia`, `wynika_z` i `jest_w_napieciu_z` od ogólnego `odwoluje_sie_do`.
6. Po tych korektach uruchomić audyt szczelności: usunięcie węzła, awaria relacji, konflikt statusu i regresja kategorii.
