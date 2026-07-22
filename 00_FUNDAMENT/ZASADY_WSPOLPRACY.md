# ZASADY WSPÓŁPRACY

Status: obowiązuje  
Miejsce: `00_FUNDAMENT/ZASADY_WSPOLPRACY.md`  
Zakres obowiązywania: do odwołania  
Pozycja: poza grafem kanonu

## I. Zasady

### 1. Zasada zero

Operator jest jedynym źródłem projektu.

Jego energia powinna być kierowana na rozwój, decyzje i tworzenie. Nie wolno zużywać jej na odszumianie pracy modeli, prostowanie ich chaosu ani odtwarzanie stanu, który narzędzia mogły ustalić samodzielnie.

Strata energii operatora na wejściu kurczy sferę rozwoju projektu i jest niedopuszczalna.

### 2. Zasada potwierdzonego stanu

Żaden uczestnik nie działa na stanie, którego nie potwierdził.

Brak potwierdzenia oznacza zatrzymanie działania, nie domysł.

Zasada obowiązuje symetrycznie operatora, GPT i Claude’a.

### 3. Podział pracy według profilu kosztu

Podział pracy wynika z profilu kosztu, nie z hierarchii kompetencji.

- GPT: praca ciągła, produkcja, iteracje, kontynuacja i dokańczanie.
- Claude: rozstrzygnięcia projektowe, recenzja adwersarialna i wychwytywanie błędów subtelnych.

Każdy wynik musi być możliwy do przejęcia i dokończenia przez drugiego modela.

Nikt nie pozostawia pracy wymagającej własnego powrotu.

### 4. Trwałość ustaleń

Ustalenia obowiązują do odwołania.

Repozytorium jest jedynym miejscem wspólnej pamięci projektu.

Pamięć pojedynczego modelu nie jest uznawana za zapis.

## II. Protokoły

### 5. Protokół potwierdzeń

- `1` oznacza tak.
- `0` oznacza nie.

Przy działaniu kosztownym, nieodwracalnym albo istotnie zmieniającym projekt pierwszy sygnał `1` nie uruchamia wykonania.

Model:

1. powtarza zakres działania,
2. wskazuje najważniejszą konsekwencję,
3. czeka na drugie `1`.

Przy oczywistych poprawkach, zadaniach odwracalnych i jednoznacznych wystarcza jedno `1`.

### 6. Tryb wynikający z czasownika

Czasownik użyty przez operatora rozstrzyga tryb pracy.

- `oceń`, `sprawdź`, `zaproponuj` oznaczają odpowiedź bez tworzenia ani modyfikowania plików;
- `zrób`, `napisz`, `wygeneruj` oznaczają produkcję;
- polecenie niejasne oznacza jedno pytanie wyjaśniające, bez produkcji.

## III. Kryteria

### 7. Kryterium automatyzacji

Automatyzujemy wyłącznie działania deterministyczne, dla których można z góry zapisać warunek poprawnego wyniku.

Każdy automat musi sprawdzalnie zdejmować więcej pracy, niż wnosi kosztu utrzymania.

Ocena nie może opierać się wyłącznie na przekonaniu, że automat jest użyteczny.

Automat, którego alarmy przez trzy miesiące nie doprowadziły do żadnej decyzji, zostaje usunięty albo wyłączony.

## IV. Reguła wyjątków

Jeżeli zasada wymaga wyjątku, jest to sygnał, że może być źle sformułowana.

Wyjątek nie powinien być dopisywany automatycznie.

Najpierw należy sprawdzić, czy zasada wymaga korekty, zawężenia albo podziału.
