# MODEL ENERGETYCZNY — SCALENIE I ERRATY v0.2

Status produkcyjny: kandydat do przebiegu głębokiego  
Status epistemiczny: propozycja robocza  
Zakres: architektura modelu, sprzężenie, dynamika, interfejs warstwy  
Przeznaczenie: duży przebieg Claude’a

# SCALENIE ERRATY I DECYZJA O ZAKRESIE MODELU

## 1. Werdykt

Errata naprawia najważniejszy błąd interpretacyjny: źródłem zmiennego obciążenia nie jest wyłącznie wnętrze pojedynczego układu, lecz jego sprzężenie z otoczeniem.

Nie domyka jednak jeszcze modelu matematycznie.

Sprzężenie zamyka **łańcuch przyczynowy**, ale nie zamyka automatycznie **układu równań**. Do pełnego domknięcia potrzebne byłoby jedno z dwóch:

1. jawne modelowanie stanu drugiej strony i reguł wzajemnego oddziaływania;
2. potraktowanie oddziaływania drugiej strony jako mierzalnego wejścia zewnętrznego.

Pierwsze rozwiązanie tworzy pełny model interakcji, ale szybko zwiększa wymiar, koszt i problem identyfikowalności. Drugie daje model otwarty, lecz operacyjnie kompletny i tani obliczeniowo.

Dla obecnego etapu właściwe jest rozwiązanie drugie.

## 2. Najważniejsze domknięcie pojęciowe

Errata pozwala ostatecznie rozdzielić `K` i `N`.

- `K(t)` jest **strumieniem kosztu wchodzącym przez granicę układu**.
- `N(t)` jest **stanem nagromadzonego, nierozładowanego napięcia wewnątrz układu**.

Nie opisują już tego samego.

`K` ma jednostkę przepływu lub obciążenia na jednostkę czasu.  
`N` jest zasobem skumulowanym.

Wtedy naturalnie:

- bieżąca interakcja zwiększa lub zmniejsza `K`;
- `K` zasila zmianę `N`;
- `C` decyduje, jaka część napływającego obciążenia zostaje przetworzona, rozładowana albo zakumulowana.

To jest najważniejszy rezultat erraty. Bez tego `K` i `N` były dwiema nazwami podobnego zjawiska. Po rozdzieleniu strumienia i stanu zaczynają tworzyć dynamikę.

## 3. Co z erraty należy przyjąć

### 3.1. Jednostką obliczeniową jest epizod sprzężenia

Model nie musi symulować całego życia układu z jednakową rozdzielczością.

Powinien rozróżniać:

- stan bazowy;
- epizod aktywnego sprzężenia;
- stan po epizodzie, gdy utrzymuje się jego konsekwencja albo prognoza kolejnego kontaktu.

To uzasadnia architekturę zdarzeniową zamiast ciągłego, kosztownego liczenia każdej chwili.

### 3.2. Obciążenie ma trzy źródła

Całkowite obciążenie graniczne można rozłożyć na:

\[
K(t)=K_0(t)+K_-(t)+K_+(t)
\]

gdzie:

- `K₀` oznacza koszt interakcji bieżącej;
- `K₋` oznacza pozostałość po interakcjach przeszłych;
- `K₊` oznacza koszt symulowania interakcji przyszłych.

To tłumaczy, dlaczego brak fizycznego kontaktu nie oznacza braku obciążenia.

Samotny układ może nadal utrzymywać otwarte sprzężenie przez pamięć, przewidywanie, oczekiwanie, przygotowanie albo niedomknięty przebieg wcześniejszego zdarzenia.

### 3.3. Matryca należy do granicy

Matryca nie powinna opisywać gotowej trajektorii.

Jej właściwą funkcją jest mapowanie cech interakcji na strumienie oddziałujące na układ:

\[
u(t)\rightarrow M u(t)\rightarrow K(t)
\]

`u(t)` jest wektorem obserwowalnych cech epizodu, na przykład:

- intensywności;
- nieprzewidywalności;
- zgodności deklaracji z przebiegiem;
- presji czasowej;
- wzajemności;
- możliwości wycofania;
- stopnia niedomknięcia.

Matryca opisuje sygnaturę energetyczną kontaktu. Trajektorię nadal generuje układ zależnie od własnego stanu.

## 4. Gdzie errata idzie za daleko

### 4.1. Dynamika graniczna powinna być założeniem zakresu, nie twierdzeniem ogólnym

Zdanie, że cała dynamika w izolacji jest importowana, jest zbyt mocne.

Układ posiada dynamikę endogenną: regenerację, rytmy biologiczne, dryf, chorobę, uczenie, spontaniczne pobudzenie, procesy pamięciowe i zmiany metaboliczne.

Nie trzeba ich jednak szczegółowo modelować.

W tej wersji należy przyjąć słabsze i obronne założenie:

> W klasie analizowanych epizodów głównym źródłem niestacjonarnego obciążenia jest sprzężenie z otoczeniem. Dynamika endogenna jest ujmowana jako baza, wolny dryf i zakłócenie.

To zachowuje redukcję obliczeniową bez składania ontologicznej deklaracji o naturze człowieka.

### 4.2. Bramka epizodu nie rozwiązuje sama problemu skal czasu

Podział na bazę i epizody rozwiązuje problem **kosztu obliczeniowego**.

Nie rozwiązuje całkowicie problemu **dynamiki czasowej**.

Nadal muszą istnieć różne szybkości procesów:

- szybki wzrost napięcia;
- wolniejszy spadek zasobu;
- jeszcze wolniejsza degradacja lub odbudowa `C`;
- zanikanie skutków poprzedniego epizodu;
- narastanie obciążenia wyprzedzającego.

Nie są konieczne osobne modele dla sekund, dni i miesięcy. Potrzebne są jednak różne stałe szybkości albo czasy zaniku. Inaczej miesięczne wyczerpanie nadal będzie matematycznie tym samym procesem co sekundowa erupcja, tylko narysowanym dłużej.

## 5. Decyzja o zakresie następnej wersji

Następna wersja powinna być zdefiniowana jako:

> Otwarty, epizodyczny model hybrydowy pojedynczego układu poddanego mierzalnemu sprzężeniu z otoczeniem.

Nie należy jeszcze modelować pełnego układu dwóch osób.

Druga strona zostaje skompresowana do obserwowalnego wejścia na granicy. Model nie próbuje zgadywać jej pełnego stanu wewnętrznego.

To oznacza:

- jeden modelowany układ;
- trzy zmienne stanu: `E`, `N`, `C`;
- jedno wejście sprzężenia, złożone z części bieżącej, przeszłej i przewidywanej;
- dwa podstawowe tryby: baza i epizod;
- jeden detektor niespójności;
- jeden warunek przeciążenia;
- profile rozpoznawane dopiero po wygenerowaniu trajektorii.

## 6. Status trzech zmiennych

### `E` — dostępny zasób

Nie oznacza abstrakcyjnej „energii emocjonalnej”, lecz zasób dostępny do podtrzymywania procesów, regulacji i odpowiedzi.

### `N` — nagromadzone nierozwiązane napięcie

Jest stanem, nie chwilowym bodźcem. Powstaje wtedy, gdy napływające obciążenie nie zostało przetworzone, rozładowane albo zakończone.

### `C` — zdolność przepływu

`C` nie jest drugim zasobem.

Jest stanem określającym, jak skutecznie układ:

- przetwarza napływające obciążenie;
- wykorzystuje dostępne `E`;
- rozładowuje `N`;
- przechodzi między pobudzeniem a powrotem do bazy.

W praktyce `C` działa jako zmienny współczynnik transmisji i regulacji.

Musi posiadać własną dynamikę. Powinno:

- spadać pod wpływem długotrwałego nierozwiązanego obciążenia;
- odzyskiwać się przy dostępności zasobu i braku nadmiernego napływu;
- wpływać zarówno na akumulację `N`, jak i wykorzystanie `E`.

Bez `dC/dt` trzecia zmienna pozostaje komentarzem do modelu, nie jego częścią.

## 7. Minimalna architektura

Łańcuch powinien wyglądać następująco:

\[
\text{cechy interakcji}
\rightarrow
\text{mapowanie sprzężenia}
\rightarrow
K(t)
\rightarrow
F(E,N,C,K)
\rightarrow
\text{trajektoria}
\rightarrow
\text{profil obserwowany}
\]

Deklaracja i rzeczywisty przebieg tworzą osobny kanał:

\[
\text{deklaracja}
+
\text{przebieg}
\rightarrow
D
\]

gdzie `D` jest miarą niespójności.

`D` nie powinno automatycznie oznaczać kłamstwa, winy ani złej intencji. Jest różnicą między dwoma kanałami danych.

Może służyć do:

- oznaczania przypadku do analizy;
- korekty wiarygodności deklarowanego wejścia;
- kalibracji matrycy sprzężenia;
- wykrywania niepełnej albo błędnej reprezentacji epizodu.

Nie powinno samo stawać się emocją ani oceną moralną.

## 8. Jeden próg zamiast katalogu progów

Nie należy teraz utrzymywać osobnych wartości `N_kryt`, `E_min` i `C_min`.

Lepiej zbudować jeden skalarny wskaźnik przeciążenia:

\[
\Omega=\Phi(E,N,C)
\]

Przejście następuje, gdy:

\[
\Omega>1
\]

Dokładna postać `Φ` zostaje do wyprowadzenia i kalibracji.

Takie rozwiązanie ma trzy zalety:

1. próg pozostaje jeden;
2. jego efektywne położenie zależy od całego stanu;
3. spadek `C` albo `E` może zwiększyć podatność bez dokładania kolejnych arbitralnych granic.

## 9. Tryb a profil

W modelu należy pozostawić tylko minimalną część dyskretną:

- tryb bazowy;
- tryb epizodu.

Opcjonalnie później można dodać tryb przeciążenia, ale dopiero jeśli jedna granica rzeczywiście rozdziela jakościowo odmienne równania.

Profil nie jest trybem.

Profil jest opisem kształtu uzyskanej trajektorii, na przykład:

- narastanie;
- wygasanie;
- oscylacja;
- załamanie;
- powrót;
- przełączenie.

Nie należy ich wpisywać do mechanizmu jako gotowej listy wyników. Mają ujawnić się w przebiegach. Dopiero po serii przypadków będzie wiadomo, które klasy są rzeczywiście rozłączne i użyteczne.

## 10. Granice matrycy

Liniowa matryca sprzężenia jest właściwa jako pierwsza warstwa:

\[
K=M u
\]

Nie powinna jednak odpowiadać za całą nieliniowość modelu.

Nieliniowość można zachować poza matrycą, przez:

- zależność odpowiedzi od `E`, `N` i `C`;
- wzmocnienie zależne od stanu;
- nasycenie;
- warunek przeciążenia;
- zmianę trybu.

Dzięki temu matryca pozostaje prosta, czytelna i kalibrowalna, a eskalacja wynika z układu, nie z ręcznego katalogu wyjątków.

## 11. Jak liczyć to tanio

Koszt obliczeń powinien zależeć od liczby epizodów, nie od długości całej historii.

### Poza epizodem

- aktualizacja stanu bazowego dużym krokiem;
- prosta funkcja regeneracji i dryfu;
- brak klasyfikowania profili;
- brak uruchamiania pełnej dynamiki interakcji.

### W epizodzie

- odczyt cech wejścia;
- jedno mnożenie macierzowe;
- aktualizacja `E`, `N`, `C`;
- obliczenie `Ω`;
- zapis trajektorii i detektora `D`.

### Pamięć przeszłości i prognoza przyszłości

Można użyć rekursywnych śladów z zanikiem zamiast przechowywania całej historii.

Obliczeniowo jest to stały koszt na epizod.

Formalnie takie ślady są dodatkowymi stanami ukrytymi. W wersji minimalnej mogą należeć do warstwy przygotowania wejścia, a nie do rdzenia `E,N,C`. Trzeba tylko uczciwie zaznaczyć, że pełny model autonomiczny miałby wtedy więcej niż trzy zmienne.

## 12. Ocena po erracie

### Rama pojęciowa

Domknięta w wysokim stopniu. Mechanika przed nazwą, emocja jako etykieta wtórna i detektor deklaracja–przebieg tworzą spójny kierunek.

### Architektura mechaniczna

Około dwóch trzecich.

Wiadomo już:

- co jest stanem;
- co jest strumieniem;
- gdzie znajduje się dynamika interakcji;
- gdzie ma działać matryca;
- czym różni się tryb od profilu;
- jak ograniczyć koszt obliczeń.

### Formalizm matematyczny

Nadal około jednej trzeciej.

Brakuje:

- jawnych prawych stron zależnych od stanu;
- `dC/dt`;
- definicji operacyjnej wejścia;
- postaci wskaźnika `Ω`;
- czasów zaniku;
- warunków identyfikowalności;
- procedury kalibracji.

### Operacjonalizacja

Najmniej rozwinięta.

Dopóki nie wiadomo, jak z obserwacji epizodu uzyskać `u(t)`, model nie może być sprawdzany na rzeczywistych przypadkach.

## 13. Zadanie dla przebiegu głębokiego

Przebieg wysokotokenowy powinien rozstrzygnąć wyłącznie:

1. równania dla `E`, `N`, `C`;
2. mechanizm sprzężenia zwrotnego między nimi;
3. własną dynamikę `C`;
4. definicję obserwowalnego wejścia `u`;
5. mapowanie `u → K`;
6. postać jednego wskaźnika przeciążenia `Ω`;
7. różne szybkości procesów;
8. granicę między jawnym stanem a pamięcią wejścia;
9. identyfikowalność parametrów;
10. test na kilku kontrastowych epizodach.

Nie należy teraz rozwijać katalogu emocji, profili ani trybów.

## 14. Decyzja końcowa

Sprzężenie domyka model **przyczynowo**, lecz nie domyka go jeszcze **autonomicznie**.

Następna wersja nie powinna próbować być autonomicznym modelem dwóch pełnych układów. Powinna być operacyjnie zamkniętym modelem otwartym, w którym otoczenie jest reprezentowane przez mierzalny sygnał graniczny.

Najważniejsza redukcja brzmi:

> Nie modelować całej drugiej strony. Modelować to, co przekracza granicę.

To zachowuje istotę mechanizmu, umożliwia pomiar i ogranicza koszt.

Pełny model dwustronny pozostaje późniejszym rozszerzeniem, uruchamianym wyłącznie wtedy, gdy wersja graniczna systematycznie nie wyjaśnia obserwowanych przebiegów.

---

# ERRATA II — SZEW I KRYTERIUM ZAMKNIĘCIA WARSTWY

## E5. Szew warstwy

Szew nie przebiega po temacie ani po granicy nazw domenowych. Przebiega po **wąskim interfejsie**, przez który warstwa przekazuje wynik wyżej i odbiera stan zwrotny.

W modelu energetycznym szwem jest sprzężenie:

- do układu wchodzi obciążenie `K`;
- z układu wychodzi stan opisany przez `E`, `N`, `C` oraz wynik progu `Ω`;
- szczegóły źródła obciążenia nie przechodzą przez szew, dopóki nie są potrzebne do jego wyznaczenia.

Somatyka, sen, pogoda, trawienie, bieżąca interakcja, ślad przeszłości i symulacja przyszłości mogą zostać sprowadzone do jednego kształtu wejścia: obciążenia na granicy.

Nie oznacza to, że są tym samym zjawiskiem. Oznacza wyłącznie, że dla tej warstwy mają wspólny interfejs.

## E6. Doprecyzowanie kierunku interfejsu

Sformułowanie „do góry idzie obciążenie, w dół stan” wymaga ustalenia orientacji warstw.

Dla tego dokumentu przyjmuje się:

- warstwa źródeł i obserwacji przekazuje do modelu wektor cech `u(t)`;
- warstwa sprzężenia mapuje `u(t)` na obciążenie `K(t)`;
- rdzeń dynamiczny zwraca stan `x(t)=[E,N,C]` oraz `Ω`;
- warstwa interpretacji może dopiero potem nadać wtórną nazwę obserwowanemu przebiegowi.

Minimalny szew rdzenia ma więc postać:

\[
K(t) \rightarrow [E(t),N(t),C(t),\Omega(t)]
\]

Detektor niespójności `D` biegnie kanałem równoległym. Nie rozszerza stanu podstawowego, dopóki nie okaże się, że wpływa na dynamikę, a nie tylko na wiarygodność wejścia.

## E7. Trzy warunki zamknięcia warstwy

Warstwa jest zamknięta dopiero wtedy, gdy jednocześnie:

1. można ją testować bez uruchamiania warstwy wyższej;
2. jej interfejs ma ustalony kształt i nie zmienia się przy dokładaniu treści niżej;
3. jej pełna aktywna definicja znajduje się w jednym dokumencie.

Trzeci warunek nie jest redakcyjnym luksusem. Rozproszenie definicji między kilkoma dokumentami oznacza, że warstwa nadal wymaga rekonstrukcji przed użyciem, więc praktycznie nie jest zamknięta.

Niniejszy dokument ma być tym jednym miejscem dla wersji roboczej modelu przed przebiegiem głębokim.

## E8. Test zamknięcia modelu

Warstwa modelu energetycznego może zostać uznana za domkniętą w pierwszej wersji, gdy:

- rzeczywiste dane epizodu dają się przekształcić do `u(t)`;
- `u(t)` daje `K(t)` bez odwołania do nazw emocji;
- równania generują przebieg `E`, `N`, `C`;
- jeden wskaźnik `Ω` daje rozstrzygnięcie progu;
- detektor `D` porównuje deklarację z przebiegiem;
- test można wykonać na danych wejściowych bez użycia warstwy interpretacyjnej.

Nazwa emocji może zostać dodana później jako etykieta opisu trajektorii. Nie uczestniczy w teście domknięcia.

## E9. Reguła eskalacji modelu

Mocniejszy model powinien wejść po ustaleniu interfejsu i kryterium testu, ale przed ogłoszeniem matematycznego zamknięcia, ponieważ właśnie jego zadaniem jest wyprowadzenie i sprawdzenie dynamiki.

Dlatego regułę Claude’a należy zastosować tu precyzyjnie:

> Mocniejszy model nie ma ponownie projektować granicy warstwy. Ma rozstrzygnąć mechanikę wewnątrz ustalonego interfejsu.

Duży przebieg Claude’a otrzymuje więc zamknięty zakres wejściowy:

- nie zmienia liczby podstawowych zmiennych bez wykazania konieczności;
- nie rozszerza interfejsu sprzężenia bez kontrprzykładu;
- nie rozwija katalogu emocji ani profili;
- nie modeluje pełnego wnętrza drugiej strony;
- ma wyprowadzić równania, definicję wejścia, próg i testy.

W tym sensie eskalacja następuje po zamknięciu **szwu i zakresu**, lecz przed zamknięciem **formalizmu matematycznego**.

## E10. Zabezpieczenie przed korkociągiem

Po przyjęciu szwu następujące elementy są zamrożone na czas przebiegu głębokiego:

- trzy podstawowe zmienne `E`, `N`, `C`;
- `K` jako strumień obciążenia na granicy;
- jeden próg złożony `Ω`;
- baza + epizody;
- profil jako wynik, nie tryb;
- nazwa emocji jako etykieta wtórna;
- jeden dokument jako aktywna definicja warstwy.

Ponowne otwarcie któregoś z tych punktów wymaga jawnego wskazania:

1. kontrprzykładu, którego obecny interfejs nie obsługuje;
2. skutku dla pozostałych elementów;
3. minimalnej koniecznej korekty.

Dobry pomysł bez kontrprzykładu trafia do sekcji rozszerzeń późniejszych, nie do bieżącego rdzenia.

## E11. Granica na dziś

Warstwa pojęciowa i interfejs są wystarczająco blisko zamknięcia, aby przekazać dokument do przebiegu wysokotokenowego.

Nie jest jeszcze zamknięta warstwa matematyczna, ponieważ nadal brakuje:

- równań zależnych od stanu;
- `dC/dt`;
- operacyjnej definicji `u(t)`;
- kalibracji mapowania `u → K`;
- postaci `Ω`;
- testu na rzeczywistych danych.

Claude nie otrzymuje zadania ponownego scalenia koncepcji. Otrzymuje zadanie domknięcia mechaniki wewnątrz ustalonego szwu.

---

# ZAKRES PRZEBIEGU GŁĘBOKIEGO CLAUDE’A

## Cel

Zbudować minimalny, testowalny układ dynamiczny działający wewnątrz ustalonego interfejsu sprzężenia.

## Obowiązkowy wynik

1. jawne równania `dE/dt`, `dN/dt`, `dC/dt`;
2. definicja obserwowalnego wejścia `u(t)`;
3. mapowanie `u(t) → K(t)`;
4. jeden wskaźnik przeciążenia `Ω(E,N,C)`;
5. różne skale szybkości procesów;
6. warunki bazowe i bramka epizodu;
7. pozycja detektora `D` w architekturze;
8. testy na co najmniej trzech kontrastowych epizodach;
9. ocena identyfikowalności parametrów;
10. jawna lista elementów, których nie da się rozstrzygnąć bez danych.

## Poza zakresem

- katalog emocji;
- katalog profili;
- pełny model dwóch osób;
- rozbudowa ontologii człowieka;
- tworzenie nowych warstw;
- ponowne projektowanie szwu bez kontrprzykładu;
- ozdobniki narracyjne.

## Kryterium zakończenia

Przebieg jest zakończony, gdy przez trzy zmienne i jeden próg przechodzą rzeczywiste albo realistyczne dane wejściowe, a model daje werdykt bez użycia nazwy emocji.
