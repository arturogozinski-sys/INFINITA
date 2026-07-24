---
dokument: SPRZECZNOSCI_PRAWO_LOGIKA_INFINITA_v0.1
status_produkcyjny: warsztat
status_epistemiczny: propozycja robocza
snapshot_bazowy: a0c6cb2
data: 2026-07-24
uwaga: NIE rozstrzygam urzędniczo ani za operatora. Każdy konflikt = warianty + decyzja wymagana.
---

# Sprzeczności prawo ↔ logika (do rozstrzygnięcia)

Format każdej pozycji: literalne brzmienie → funkcja chroniona → obecny skutek → skutek uboczny → wariant wg litery → wariant wg ducha → wariant logicznie najlepszy → decyzja wymagana od operatora.

---

## C-α — Reguła kroku (K7) × jawna niepewność (K4)

- **Litera:** K7 — krok bez wpływu na niepewność/decyzję/ryzyko/wyjście jest zbędny. K4 — niepewność oznaczaj, waliduj źródła, nie skracaj dowodu.
- **Funkcja chroniona:** K7 — wydajność. K4 — wiarygodność.
- **Obecny skutek:** brak jawnej granicy „zbędny obieg" vs „ucięta weryfikacja".
- **Skutek uboczny:** ryzyko, że optymalizacja przepływu utnie krok dowodowy i wyprodukuje pozorną pewność.
- **Wariant wg litery:** trzymać oba, licząc, że nie kolidują.
- **Wariant wg ducha:** tnij obiegi, nigdy nie tnij dowodu istotnego dla decyzji.
- **Wariant logicznie najlepszy:** krok walidacyjny liczy się jako „zmniejsza niepewność" — więc nie jest zbędny z definicji; próg cięcia = koszt błędu (A §4).
- **Decyzja wymagana:** zatwierdzić regułę „walidacja proporcjonalna do kosztu błędu jest zawsze krokiem koniecznym"? (tak/nie)

## C-δ — Operator-źródło (K1) × rygor rozdziału i niepewności (K3/K4)

- **Litera:** K1 — chroń energię operatora, wejście utylitarne, duże przesiewy. K3/K4 — rozdzielaj warstwy, oznaczaj niepewność (kosztuje kroki).
- **Funkcja chroniona:** K1 — sprawność źródła. K3/K4 — niezafałszowany obraz.
- **Obecny skutek:** napięcie: tani przesiew vs pełny rygor przy każdym materiale.
- **Skutek uboczny:** albo przeciążony operator, albo spłycony rygor.
- **Wariant wg litery:** stosować pełny rygor zawsze (K3/K4 literalnie).
- **Wariant wg ducha:** rygor proporcjonalny do rangi i kosztu błędu; drobna sprawa zostaje drobną.
- **Wariant logicznie najlepszy:** próg rygoru sterowany klasyfikacją z bramy wejściowej (ranga → poziom rygoru).
- **Decyzja wymagana:** kto/co ustawia próg rygoru — reguła automatyczna z klasyfikacji, czy operator per sprawa? (wybór)

## C1 — Budżet MANIFEST_ZADANIA × logika uspójnienia całości

- **Litera:** MANIFEST_ZADANIA §4 — „max 10 plików, 3000 linii, zakaz czytania całego repozytorium".
- **Funkcja chroniona:** koszt kontekstu, ochrona energii (K1), brak rozłażenia zadania.
- **Obecny skutek:** audyt całościowy (Zadanie 4: który dokument opisuje ten sam organizm) formalnie nie mieści się w budżecie.
- **Skutek uboczny:** albo łamiemy budżet, albo nie wolno uspójnić struktury.
- **Wariant wg litery:** nie robić przeglądu całościowego; zostać przy 10 plikach.
- **Wariant wg ducha:** budżet chroni przed marnotrawstwem, nie przed konieczną, jednorazową syntezą.
- **Wariant logicznie najlepszy:** budżet skalowany do rangi zadania; zadanie „uspójnienie struktury" ma własny, wyższy limit z jawnym uzasadnieniem.
- **Decyzja wymagana:** czy wprowadzić kategorię „zadanie strukturalne" z podniesionym budżetem? (tak/nie)

## C2 — S002 (wersja NIE w nazwie pliku) × praktyka dokumentów roboczych

- **Litera:** S002 — „Nazwa pliku aktywnego dokumentu odpowiada jego identyfikatorowi... Tytuł i wersja w nagłówku YAML, nie w nazwie pliku."
- **Funkcja chroniona:** stały identyfikator, brak przenumerowań, porządek ID w kanonie.
- **Obecny skutek:** dokumenty robocze łamią to wprost: `ARCHITEKTURA_POMOSTU_..._v0.1.md`, `MODEL_ENERGETYCZNY_..._v0.2` — wersja w nazwie.
- **Skutek uboczny:** albo robocze są „niezgodne z prawem", albo S002 nie obejmuje `robocze/`.
- **Wariant wg litery:** zmusić robocze do schematu ID (M/S/Z...+cyfry, bez wersji w nazwie).
- **Wariant wg ducha:** S002 chroni **kanon** przed chaosem ID; `robocze/` to szkice bez rygoru (FUNDAMENT: „robocze — bez rygoru") — poza zakresem S002.
- **Wariant logicznie najlepszy:** jawnie zapisać zakres S002 = tylko `kanon/`; `robocze/` ma własną, luźną konwencję (wersja w nazwie dozwolona).
- **Decyzja wymagana:** potwierdzić, że S002 obejmuje wyłącznie `kanon/`? (tak/nie)

## C3 — Hierarchia rang (AUDYT_RANG) × logika jako prawo najwyższe (K0)

- **Litera:** AUDYT_RANG — hierarchia: metakanon/konstytucja → S → Z → M → P → I. Brak „logiki" jako szczebla.
- **Funkcja chroniona:** czytelny porządek nadrzędności dokumentów.
- **Obecny skutek:** najwyższy jest dokument (metakanon), nie zasada rozumu.
- **Skutek uboczny:** możliwe „przepis mówi" ponad logiką — dokładnie to, co ten przebieg odrzuca.
- **Wariant wg litery:** logika nie ma rangi; rozstrzyga najwyższy dokument.
- **Wariant wg ducha:** dokumenty służą rozumowi; logika jest ponad nimi jako test.
- **Wariant logicznie najlepszy:** dodać K0 jako meta-warstwę **nad** hierarchią dokumentów (nie jako kolejny dokument w szeregu).
- **Decyzja wymagana:** ratyfikować logikę jako meta-warstwę nad rangami? (tak/nie) — uwaga: to zmiana prawodawstwa, wymaga Twojej kontrasygnaty.

## C4 — Kolejność źródeł (instrukcja §2) × kolejność tego przebiegu

- **Litera:** instrukcja projektu §2 — przy różnicy wygrywa: 1) aktualny plik w `kanon/`, 2) dokument nadrzędny, 3) inny plik repo, 4) baza wiedzy...
- **Funkcja chroniona:** jedno źródło prawdy o stanie, brak równoległego kanonu.
- **Obecny skutek:** `kanon/` rozstrzyga przed logiką i spójnością funkcjonalną.
- **Skutek uboczny:** przypadkowy historycznie zapis w `kanon/` blokuje logicznie lepszą strukturę.
- **Wariant wg litery:** `kanon/` zawsze wygrywa, nawet gdy niespójny.
- **Wariant wg ducha (deklaracja operatora tego przebiegu):** logika → spójność funkcjonalna → kanony nienegocjowalne → dopiero potem struktura formalna.
- **Wariant logicznie najlepszy:** rozdzielić dwie osie: `kanon/` pozostaje źródłem prawdy o **aktualnym stanie**; logika rozstrzyga o **kierunku przebudowy**. Nie mieszać „co jest" z „co ma być".
- **Decyzja wymagana:** zatwierdzić rozdział osi „stan (kanon/)" vs „kierunek (logika)"? (tak/nie)

## C5 — Wyjątek ostrzegawczy (K2, A §10) × logika najwyższa (K0), etyka nie ponad logiką

- **Litera:** A §10 — w bezpośrednim, poważnym zagrożeniu system może działać przed pełną analizą (przerwać trajektorię do szkody).
- **Funkcja chroniona:** ochrona życia/sprawczości w skrajnym przypadku.
- **Obecny skutek:** jeden punkt, w którym etyka wyprzedza pełne rozumowanie.
- **Skutek uboczny:** wygląda jak „etyka ponad logiką", co koliduje z K0.
- **Wariant wg litery:** etyka ma tu priorytet nadrzędny.
- **Wariant wg ducha:** to nie etyka ponad logiką — to logika uznająca, że w wąskim zakresie koszt zwłoki > koszt niepełnej analizy.
- **Wariant logicznie najlepszy:** przeformułować wyjątek jako **wniosek logiczny** (analiza kosztu błędu), nie jako etyczny nakaz nad logiką; zakres skrajnie wąski, natychmiastowy zwrot sprawczości.
- **Decyzja wymagana:** przyjąć, że wyjątek ostrzegawczy jest decyzją logiczną o koszcie zwłoki, a nie etyką ponad logiką? (tak/nie)

## C6 — Geneza nie była planem: dokumenty opisujące ten sam organizm

- **Litera:** obecny podział katalogów i osobne dokumenty (K3, K5, K8 jako trzy; M045/M046 rozdzielone; M003/M018/M044 z procedurami w środku wg AUDYT_RANG).
- **Funkcja chroniona:** rozdział funkcji, jedna funkcja na dokument.
- **Obecny skutek:** trzy kanony (K3/K5/K8) opisują jeden organizm „granice wnioskowania" z różnych stron; kilka M zawiera ukryte procedury (proces przejął częściowo funkcję zasady).
- **Skutek uboczny:** albo sztuczne mnożenie bytów, albo scalenie zamaskowałoby realną różnicę funkcji.
- **Wariant wg litery:** zostawić podział katalogów jako przyszły podział funkcjonalny.
- **Wariant wg ducha:** podział katalogów ≠ podział funkcjonalny; sprawdzić komplementarność, nie zakładać rozłączności.
- **Wariant logicznie najlepszy:** oznaczyć K3/K5/K8 jako fasety jednego kanonu „granice wnioskowania" (bez scalania teraz); wydzielić ukryte procedury z M do P dopiero, gdy mają samodzielną funkcję (zgodnie z własną rekomendacją AUDYT_RANG).
- **Decyzja wymagana:** zgoda na kandydowanie K3/K5/K8 do wspólnego kanonu i przegląd „proces vs zasada" w M003/M018/M044? (tak/nie)

## C7 — Dobór zasad jako kontekst (ostrzeżenie K0)

- **Litera:** brak zapisu; to luka.
- **Funkcja chroniona (docelowo):** neutralność doboru zasad tworzących kontekst decyzji.
- **Obecny skutek:** ten sam zestaw kanonów, inaczej dobrany do sprawy, daje inne rozstrzygnięcie — bez jawnej reguły doboru.
- **Skutek uboczny:** pole na tendencje i przeciążenia (Twoje sformułowanie); etyka „przemyca się" nie przez kolizję z logiką, lecz przez selekcję przesłanek.
- **Wariant wg litery:** brak — nie ma zapisu.
- **Wariant wg ducha:** dobór zasad musi być jawny i uzasadniony funkcją sprawy, nie intuicją.
- **Wariant logicznie najlepszy:** reguła: dla każdej decyzji zapisać, które kanony tworzą kontekst i dlaczego (ślad doboru, K10), by dobór był audytowalny.
- **Decyzja wymagana:** wprowadzić „ślad doboru zasad" jako wymóg przy decyzjach spornych? (tak/nie)

---

## Podsumowanie decyzji wymaganych (do dyskusji, nie do wykonania)

C-α, C-δ, C1–C7: dziewięć rozstrzygnięć. Trzy są **prawodawcze** (zmieniają prawo projektu): C3 (logika jako meta-warstwa), C4 (rozdział osi stan/kierunek), C7 (ślad doboru zasad). Pozostałe są **porządkujące** (zakres S002, budżet strukturalny, status wyjątku ostrzegawczego, fasety K3/K5/K8).

Żadnego nie rozstrzygam. To grunt pod świadome przepisanie prawa po rozpoznaniu nienegocjowalnych podstaw.
