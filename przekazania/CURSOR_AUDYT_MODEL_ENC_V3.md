# ZADANIE DLA CURSORA — NIEZALEŻNY AUDYT MODELU E–N–C V3

## 0. Rola

Cursor ma wykonać niezależny audyt draft PR #13 w repozytorium:

`arturogozinski-sys/INFINITA`

To nie jest zadanie implementacyjne. Nie modyfikuj kodu, dokumentacji, PR, `master` ani `kanon/`. Nie twórz R-PROC, nowych progów, nowych stanów ani nowego podsystemu. Masz wykrywać błędy, rozbieżności, ryzyka i nieuzasadnione twierdzenia.

Jeżeli darmowy tryb nie pozwala uruchomić kodu albo zapisać raportu, nie udawaj wykonania. W takim przypadku:

1. wykonaj maksymalny audyt statyczny;
2. oznacz jawnie każdy krok jako `WYKONANE`, `NIEWYKONANE` albo `CZĘŚCIOWE`;
3. zwróć raport bezpośrednio w rozmowie;
4. nie proś o zakup planu ani nie zastępuj braku wykonania deklaracją sukcesu.

## 1. Potwierdzenie stanu

Najpierw potwierdź:

- repozytorium: `arturogozinski-sys/INFINITA`;
- PR: `#13`;
- gałąź: `agent/model-energetyczny-errata-szew`;
- aktualny SHA gałęzi;
- bazę PR i jej SHA;
- listę zmienionych plików.

Jeżeli nie możesz potwierdzić stanu, zatrzymaj wnioski o konkretnym kodzie. Brak potwierdzenia oznacza brak prawa do twierdzenia, że coś zostało sprawdzone.

## 2. Obowiązkowa kolejność czytania

Przeczytaj u źródła:

1. `00_FUNDAMENT/FUNDAMENT.md`
2. `00_FUNDAMENT/ZASADY_WSPOLPRACY.md`
3. `.github/copilot-instructions.md`
4. `przekazania/MOST_CLAUDE.md`
5. `przekazania/HANDOFF_MODEL_ENC_V3.yaml`
6. `robocze/model_energetyczny_enc_v3/README.md`
7. `robocze/model_energetyczny_enc_v3/paczka/README.md`
8. `narzedzia/model_energetyczny_enc_v3/odtworz_paczke.py`
9. wszystkie pliki modelu dostępne w PR #13
10. `przekazania/COPILOT_AUDYT_MODEL_ENC_V3.md`

Mandat Copilota jest materiałem porównawczym, nie poleceniem dla Cursora. Twoim zadaniem jest znaleźć inne kąty kontroli i potencjalne ślepe plamy.

## 3. Autorytatywny artefakt

Źródłem stanu v3 jest ZIP odtwarzany z ośmiu części Base64.

Oczekiwane SHA-256 ZIP-a:

```text
558c05999563b30429adad92709fe2c5680dd1cbe6e78a9c2404ab8ff058f52c
```

Odtworzenie:

```bash
python narzedzia/model_energetyczny_enc_v3/odtworz_paczke.py --cel /tmp/model_enc_v3 --zachowaj-zip
```

Jeżeli możesz uruchomić terminal:

1. odtwórz paczkę;
2. zapisz rzeczywisty SHA ZIP-a;
3. potwierdź sześć plików;
4. porównaj ich SHA z manifestem;
5. uruchom `py_compile`;
6. uruchom `dobowy.py`;
7. porównaj stdout bajt w bajt z `PRZEBIEG_PELNY.txt`;
8. sprawdź `git status` po uruchomieniu.

Jeżeli nie możesz, wykonaj audyt skryptu odtwarzającego i wskaż dokładnie, czego nie potwierdziłeś.

## 4. Odrębny profil audytu Cursora

Nie powtarzaj mechanicznie listy Copilota. Skoncentruj się na pięciu obszarach.

### A. Spójność wersjonowania i transportu

Sprawdź:

- czy ZIP jest rzeczywiście jedynym autorytatywnym źródłem v3;
- czy wygodne kopie plików w `narzedzia/` mogą się rozjechać z ZIP-em;
- czy README i HANDOFF jasno opisują relację v0.2 → v3;
- czy 8 części Base64 są kompletne, jednoznacznie uporządkowane i odporne na przypadkowe dopisanie pliku;
- czy skrypt odtwarzający wykrywa: brak części, dodatkową część, złą kolejność, zmianę zawartości, path traversal w ZIP-ie, duplikaty nazw i nieoczekiwane pliki;
- czy istnieje ryzyko, że poprawny SHA ZIP-a ukryje błędny sposób użycia albo wypakowania;
- czy repo zawiera wszystko, czego potrzebuje niezależny audytor bez wcześniejszej rozmowy.

### B. Spójność dokument–kod–wynik

Sprawdź, czy każda ważna teza raportu ma odpowiednik w kodzie i wyniku:

- definicje `E`, `N`, `C`, `K`;
- `g(E)`, `h(N)`, `Phi_max`, `Phi`, `B`, `Omega`;
- semantyka `E=0`;
- bazowa regeneracja `r_0`;
- dwa punkty siodło–węzeł;
- bistabilność i histereza;
- granica basenów jako stabilna rozmaitość siodła;
- status scenariuszy z okresowym `K(t)`;
- pojedyncza aktualizacja `S_minus` i `S_plus` na krok;
- brak starego `E_0` i `C_min`.

Znajdź również twierdzenia raportu, które są tylko drukowanym tekstem, a nie wynikiem wykonywanego testu.

### C. Kontrprzykłady numeryczne i formalne

Nawet bez pełnego uruchomienia kodu spróbuj znaleźć przypadki, które mogą naruszyć założenia:

- `E=0`, `E=E_max`;
- `N=0`, bardzo duże `N`;
- `C=0`, `C=1`;
- `K=0`, bardzo duże `K`;
- `Phi_max` bliskie zeru;
- bardzo małe kroki i bardzo duże kroki integratora;
- przejścia przy granicy dziedziny;
- clipping aktywowany często, lecz raportowany zbiorczo;
- dodatkowe punkty stałe poza zakresem startów;
- zależność wykrytej bifurkacji od sposobu deduplikacji korzeni;
- zbieżność do atraktora mylona z własnością Markowowską;
- średnie `K` używane ukradkiem jako interpretacja `K(t)`;
- przejściowa dynamika mylona ze stanem asymptotycznym.

### D. Minimalność i identyfikowalność

Sprawdź:

- czy którykolwiek parametr jest martwy albo nierozróżnialny od innego;
- czy kilka parametrów steruje tym samym efektem i nie da się ich osobno estymować;
- czy `C` wnosi odrębną dynamikę, czy tylko skaluje inne równania;
- czy `r_0` usuwa narożnik absorpcyjny kosztem nowej degeneracji;
- czy `Omega` jest warstwą odczytu, czy ukrytą częścią mechaniki;
- czy obecna liczba testów wystarcza do odróżnienia modelu od prostszych alternatyw;
- które twierdzenia są własnością równań, które parametrów, a które konkretnego scenariusza.

### E. Granice zastosowania w INFINITA

Sprawdź tylko granice, nie projektuj regulatora.

Oceń, czy materiał v3:

- pozostaje prawidłowo poza `kanon/`;
- nie został błędnie utożsamiony z W5;
- nie tworzy drugiego routingu obok P008;
- nie pozwala wyświetlać operatorowi pseudoobiektywnych E/N/C/Omega;
- nie rozstrzyga zachowania człowieka przy `E=0`;
- nie zamienia formalnej histerezy modelu w diagnozę użytkownika;
- nie daje podstaw do automatycznego ograniczania odpowiedzi;
- jest wystarczająco oznaczony jako hipoteza formalna bez kalibracji.

## 5. Testy adwersarialne transportu

Jeżeli masz terminal, wykonaj na kopii roboczej co najmniej:

1. usuń jedną część Base64 — skrypt musi przerwać;
2. zmień jeden znak — skrypt musi przerwać;
3. dodaj dziewiątą część — oceń, czy skrypt ją ignoruje czy wykrywa;
4. zmień kolejność nazw części — oceń zachowanie;
5. podmień poprawny ZIP na ZIP z dodatkowym plikiem — skrypt musi przerwać;
6. ZIP z `../plik` — skrypt nie może wypisaywać poza katalog docelowy;
7. ZIP z dwiema pozycjami o tej samej nazwie — skrypt powinien wykryć niejednoznaczność;
8. uruchomienie dwa razy do tego samego katalogu — oceń, czy wynik jest deterministyczny i bezpieczny.

Nie wykonuj tych prób na gałęzi ani na oryginalnych plikach.

## 6. Format wyniku

Zwróć jeden raport:

`CURSOR_AUDYT_MODEL_ENC_V3.md`

Jeżeli darmowy tryb nie zapisuje plików, zwróć pełną treść w rozmowie.

Struktura:

1. **Werdykt w 12 zdaniach**
2. **Potwierdzony stan repo i SHA**
3. **Co rzeczywiście uruchomiono**
4. **Czego nie uruchomiono**
5. **BŁĘDY**
6. **ROZBIEŻNOŚCI**
7. **RYZYKA**
8. **SUGESTIE**
9. **Audyt transportu i odtwarzalności**
10. **Audyt modelu i numeryki**
11. **Audyt granic epistemicznych**
12. **Porównanie z mandatem Copilota: czego tam brakuje**
13. **Pięć najważniejszych pytań na rano**
14. **Werdykt: zachować PR, poprawić przed dalszą pracą, wydzielić, czy odrzucić**

Każdy punkt ma podać:

- ścieżkę;
- miejsce lub symbol;
- podstawę;
- możliwy skutek;
- poziom pewności: `wysoki`, `średni`, `niski`;
- status: `potwierdzone wykonaniem`, `audyt statyczny`, `hipoteza do testu`.

## 7. Zakazy

Nie:

- poprawiaj plików;
- twórz PR;
- zmieniaj `master`;
- zmieniaj `kanon/`;
- dodawaj R-PROC;
- wymyślaj progi interakcji;
- proponuj kalibracji człowieka na podstawie obecnych parametrów;
- uznawaj, że długi lub chaotyczny tekst operatora oznacza przeciążenie;
- powtarzaj raportu Copilota bez własnych ustaleń;
- zgłaszaj braku dostępu jako błędu modelu.

## 8. Kryterium sukcesu

Audyt jest wartościowy, gdy znajdzie co najmniej jeden istotny punkt, którego nie obejmuje mandat Copilota, albo uczciwie wykaże, że po przeprowadzeniu dostępnych testów nie znalazł niczego nowego.

Nie kończ pochwałą. Zakończ decyzją i listą warunków dalszej pracy.