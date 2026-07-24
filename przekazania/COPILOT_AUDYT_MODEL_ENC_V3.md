# ZADANIE DLA GITHUB COPILOT — AUDYT MODELU E–N–C V3

## Rola i mandat

Wykonaj techniczny i adwersarialny code review draft PR #13. Nie zmieniaj kodu, dokumentacji ani kanonu. Nie scalaj PR. Najpierw potwierdź aktualny SHA gałęzi i przeczytaj:

1. `00_FUNDAMENT/FUNDAMENT.md`
2. `00_FUNDAMENT/ZASADY_WSPOLPRACY.md`
3. `.github/copilot-instructions.md`
4. `przekazania/MOST_CLAUDE.md`
5. `przekazania/HANDOFF_MODEL_ENC_V3.yaml`
6. `robocze/model_energetyczny_enc_v3/README.md`
7. wszystkie pliki modelu i raportu z PR #13

Klasyfikuj ustalenia wyłącznie jako `BŁĄD`, `RYZYKO`, `ROZBIEŻNOŚĆ` albo `SUGESTIA`. Każdy punkt ma wskazywać plik, miejsce, podstawę i skutek.

## A. Potwierdzenie stanu i reprodukcja

1. Potwierdź, że importowane pliki mają SHA-256 zgodne z README.
2. Uruchom `python -m py_compile narzedzia/model_energetyczny_enc_v3/*.py`.
3. Uruchom `dobowy.py` z czystego checkoutu i zapisz pełne stdout.
4. Porównaj stdout bajt w bajt z `PRZEBIEG_PELNY.txt`.
5. Sprawdź, czy uruchomienie nie zmienia drzewa roboczego.
6. Podaj czas, użyte wersje Pythona i bibliotek oraz ewentualne ostrzeżenia.
7. Nie uznawaj sukcesu, jeśli którykolwiek krok nie został rzeczywiście wykonany.

## B. Matematyka i numeryka

1. Zweryfikuj niezmienniczość dziedziny `E∈[0,E_max]`, `N≥0`, `C∈[0,1]` zarówno analitycznie, jak i numerycznie.
2. Sprawdź przypadki graniczne `E=0`, `E=E_max`, `N=0`, `C=0`, `C=1`, `K=0` oraz duże `K`.
3. Zbadaj dzielenie przez małe wartości i wszystkie miejsca potencjalnego NaN/Inf.
4. Sprawdź implementację `Phi_max`, `Phi`, `B`, `g(E)`, `h(N)` i `Omega` względem raportu.
5. Niezależnie znajdź punkty stałe dla siatki `K`, używając co najmniej dwóch strategii inicjalizacji.
6. Niezależnie wyznacz oba punkty siodło–węzeł przez układ `F=0` i `det(J)=0`, nie tylko przez skan liczby korzeni.
7. Porównaj progi z raportem `0,125795` oraz `0,326309`.
8. Sprawdź wartości własne, kierunki stabilne/niestabilne i prawidłowość określenia granicy basenów jako stabilnej rozmaitości siodła.
9. Zbadaj wrażliwość wyników na tolerancję, krok różnicowy, liczbę punktów startowych, integrator i krok czasowy.
10. Sprawdź, czy clipping nie maskuje błędu albo nie generuje sztucznych atraktorów; raportuj liczbę jego uruchomień.
11. Sprawdź możliwość pominięcia dodatkowych punktów stałych poza zakresem startów.
12. Zweryfikuj lokalny test odporności parametrów; wskaż parametry, dla których okno bistabilności jest najbardziej kruche.
13. Sprawdź, czy raport nie przedstawia połowy przedziału bisekcji jako całkowitej niepewności metody.
14. Wskaż wszystko, czego `dobowy.py` tylko drukuje jako tekst, ale realnie nie oblicza.

## C. Warstwa przebiegu i śladów

1. Sprawdź, czy `S_minus` i `S_plus` są aktualizowane dokładnie raz na krok.
2. Sprawdź kolejność: wstrzyknięcie, dyskontowanie, mapowanie do `K`, integracja rdzenia.
3. Znajdź przypadki podwójnego dyskontowania, pomijania zastrzyku albo zależności od kolejności zdarzeń.
4. Sprawdź, czy jednostki i znaki `K0`, `K_minus`, `K_plus` są spójne.
5. Zweryfikuj scenariusze S1–S3 i wszystkie liczby tabel P1–P4, T1–T11.
6. Potwierdź, że S1 i S2 mają identyczny tylko ciężki blok 13 JCM, nie cały pierwszy okres.
7. Wskaż każdą interpretację średniego `K`, która sugeruje równoważność z wymuszeniem `K(t)`.
8. Sprawdź, czy istnieją dwa stabilne cykle okresowe; jeśli nie analizujesz mapy Poincarego, oznacz to jawnie jako niezweryfikowane.
9. Zbadaj wpływ fazy, kolejności bloków i długości okresu na wynik.
10. Sprawdź zachowanie po bardzo długiej symulacji i po przełączeniu stanu początkowego między gałęziami.

## D. Semantyka i dokumentacja

1. Porównaj każde równanie raportu z implementacją.
2. Porównaj każdy parametr i jego wartość.
3. Sprawdź, czy `E=0` nie zostało opisane jako biologiczne wyczerpanie lub decyzja o zachowaniu.
4. Sprawdź, czy `r_0` jest nazwane bazową/homeostatyczną regeneracją, nie odpoczynkiem.
5. Sprawdź, czy JCM nie ma przypisanej fizycznej godziny.
6. Sprawdź, czy raport nie twierdzi empirycznej wystarczalności trzech zmiennych.
7. Sprawdź, czy progi bifurkacyjne nie są przedstawione jako progi człowieka.
8. Sprawdź, czy `Omega=1` nie jest mylone z progami siodło–węzeł.
9. Wyszukaj pozostałości `E_0`, `C_min`, „rezerwy nieredukowalnej” i starej narracji.
10. Wskaż ręcznie wpisane liczby, które nie mają odtwarzalnej ścieżki obliczeniowej.
11. Sprawdź zgodność README, HANDOFF, raportu, kodu i stdout.

## E. Architektura repo i wersjonowanie

1. Oceń, czy podział `robocze/` i `narzedzia/` jest zgodny z fundamentem.
2. Sprawdź, czy snapshot nie dubluje aktywnego źródła bez wskazania relacji do v0.2.
3. Wskaż martwe lub błędne odwołania po dodaniu plików.
4. Uruchom pełne testy i kroki CI repo związane z integralnością.
5. Sprawdź, czy testy nie zmieniają drzewa roboczego.
6. Oceń, czy pliki powinny pozostać w PR #13 czy zostać wydzielone, ale nie wykonuj przeniesienia.
7. Sprawdź, czy PR nadal jest przejmowalny, minimalny i nie dotyka kanonu.
8. Nie proponuj automatycznego merge.

## F. Red-team

Szukaj co najmniej:

- błędu znaku;
- błędu jednostek;
- ukrytej zależności od clippingu;
- pominiętego korzenia;
- sztucznej bistabilności numerycznej;
- niestabilności zależnej od integratora;
- fałszywej reprodukowalności;
- wartości drukowanej, lecz nieobliczonej;
- rozjazdu dokument–kod–wynik;
- błędnego uogólnienia `K=const` na `K(t)`;
- pomieszania punktu siodłowego z całą granicą basenów;
- pamięci poza `(E,N,C)` ukrytej w wejściu;
- diagnozy operatora lub człowieka przemyconej przez nazwy zmiennych;
- niejawnej zmiany zakresu z modelu formalnego na regulator interakcji;
- zbędnego rozszerzenia architektury repo.

## Format odpowiedzi

Zostaw review PR #13 z sekcjami:

1. **Werdykt techniczny**
2. **Wykonane polecenia i faktyczne wyniki**
3. **BŁĘDY blokujące**
4. **RYZYKA istotne**
5. **ROZBIEŻNOŚCI dokument–kod–wynik**
6. **SUGESTIE nieblokujące**
7. **Macierz twierdzenie → dowód/test → wynik**
8. **Czego nadal nie zweryfikowano**
9. **Rekomendacja: zostawić draft / poprawić / wydzielić / zamknąć**

Nie twórz nowej implementacji i nie poprawiaj plików. Twoją pracą jest przetrzepać obecny stan, nie wyprodukować następny model.
