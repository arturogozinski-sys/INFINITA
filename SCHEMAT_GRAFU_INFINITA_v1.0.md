# SCHEMAT GRAFU INFINITA

Wersja: 1.0 · Status: dokument normatywny (model danych) · Para: `schemat_grafu.json` (kontrakt maszynowy)
Wersjonowany wg Konstytucji Technicznej, sekcja IX: zmiana typów, relacji lub identyfikatorów podbija wersję schematu. Ten dokument to proza dla decyzji; `schemat_grafu.json` to ten sam kontrakt dla parsera. Muszą pozostać zgodne — rozjazd łapie walidator.

## Po co schemat

Parser bez schematu przetwarza poprawnie także elegancko opisany nonsens: sprawdza składnię (czy da się sparsować), nie znaczenie (czy „mechanizm" ma to, co mechanizm mieć musi). Schemat jest kontraktem danych — zamienia „przetwarza cokolwiek" w „przetwarza tylko to, co ma sens". Egzekwuje go walidator jako część walidacji automatycznej w procesie produkcji.

## System identyfikatorów

Wzorzec: prefiks literowy (1–3 znaki) + trzy cyfry, np. `M045`. Prefiks oznacza typ. Identyfikator jest **stały**: nigdy nie jest przenumerowywany ani używany ponownie (dyscyplina wersji — Konstytucja, zasada 7).

| Prefiks | Typ |
|---|---|
| S | specyfikacja |
| M | mechanizm |
| P | proces |
| Z | zasada |
| E | dowód |
| C | przypadek |
| D | dialog |
| I | indeks |
| H | hipoteza |

## Dwie osie statusu (nie jedna)

Status produkcyjny i epistemiczny to dwie różne rzeczy — mieszanie ich to ten sam błąd, co mieszanie produktu z integracją w modelu Sfery.

**Status produkcyjny** — gdzie w łańcuchu produkcji jest element: `warsztat` / `kandydat` / `kanon` / `archiwum`. Parser kanonu przyjmuje wyłącznie `kanon`.

**Status epistemiczny** — pewność poznawcza: `propozycja` / `hipoteza` / `zweryfikowane` / `odrzucone` / `demonstracyjne`. Do kanonu wchodzi tylko `zweryfikowane`. `demonstracyjne` to fikstury prototypu — nigdy kanon.

Element w kanonie musi mieć jednocześnie status produkcyjny `kanon` i epistemiczny `zweryfikowane`. To dwustopniowa bramka: przeszedł proces (produkcyjny) i został zweryfikowany (epistemiczny).

## Typy węzłów i pola wymagane

**Kanon trwały** (pełna linia produkcji):
- **mechanizm (M)** — reguła działania. Wymaga: id, typ, tytul, status_epistemiczny, wersja. Opcjonalnie: zrodla, odwolania.
- **zasada (Z)** — zasada uniwersalna. Pola jak mechanizm.
- **specyfikacja (S)** — standard/protokół. Wymaga: id, typ, tytul, status_epistemiczny, wersja.
- **proces (P)** — procedura. Pola jak specyfikacja.

**Materiał odniesienia** (lżejsza linia):
- **dowód (E)** — wspiera mechanizmy. Wymaga: id, typ, tytul, status_epistemiczny, wiarygodnosc (1–5). Uwaga prywatności: treść dowodów bywa osobista, poza kanonem publicznym.
- **przypadek (C)** — studium przypadku. Wymaga: id, typ, tytul, status_epistemiczny.
- **dialog (D)** — zapis dialogu. Pola jak przypadek.

**Rejestr propozycji** (osobny zbiór, nie kanon):
- **hipoteza (H)** — element rejestru propozycji. Status epistemiczny w {propozycja, hipoteza}. Nie wchodzi do kanonu.

## Typy krawędzi

- **odwoluje_sie_do** — ogólne odniesienie A→B (z pola `odwolania`).
- **wspiera** — dowód wspiera mechanizm E→M (z pola `zrodla`).
- **syntetyzuje_z** — zasada powstała z syntezy wielu elementów.
- **wynika_z** — element pochodny od innego.

## Reguły integralności (egzekwowane walidatorem)

- Każdy węzeł ma typ ze słownika.
- Prefiks identyfikatora odpowiada typowi (E przy typie mechanizm → naruszenie).
- Wszystkie pola wymagane danego typu obecne i niepuste.
- Status epistemiczny z dozwolonych.
- Węzeł w kanonie: status epistemiczny = zweryfikowane.
- Hipoteza nie ma statusu produkcyjnego kanon.
- Martwa krawędź (odwołanie do nieistniejącego węzła) → ostrzeżenie, nie błąd (cel może być poza bieżącym zakresem).

## Zgodność prozy z kontraktem

Ten dokument i `schemat_grafu.json` opisują ten sam schemat. Kontraktem wykonawczym jest JSON — to on jest czytany przez walidator. Proza służy decyzjom i przeglądowi. Przy zmianie schematu zmienia się oba, z podbiciem wersji; niezgodność między nimi jest wykrywalna (walidator działa wg JSON, więc proza rozjechana z JSON zostanie zauważona przy przeglądzie).
