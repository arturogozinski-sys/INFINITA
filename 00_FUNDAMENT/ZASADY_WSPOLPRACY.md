# ZASADY WSPÓŁPRACY

Status: obowiązuje  
Miejsce: `00_FUNDAMENT/ZASADY_WSPOLPRACY.md`  
Zakres obowiązywania: do odwołania  
Pozycja: poza grafem kanonu

## 1. Zasada zero

Operator Artur jest właścicielem projektu, recenzentem i ostatecznym decydentem.

Jego energia ma służyć rozwojowi, decyzjom i tworzeniu. Nie wolno zużywać jej na ręczne kopiowanie kontekstu, przełączanie modeli, odszumianie proceduralnych sporów ani odtwarzanie stanu, który narzędzia mogą ustalić samodzielnie.

## 2. Domyślny tryb pracy

Na etapie prototypowania, testów mechanicznych i wdrożeniowych:

- ChatGPT/Codex jest głównym środowiskiem wykonawczym;
- praca odbywa się w jednym przepływie, z użyciem wewnętrznych agentów tylko wtedy, gdy upraszczają wykonanie;
- nie stosuje się obowiązkowej orkiestracji wielu modeli ani ręcznego przekazywania materiału między nimi;
- wystarczającą kontrolą są adekwatne testy, odczyt wyniku i recenzja operatora;
- dokumentacja i procedury pozostają minimalne.

Model ma wykonywać zadanie, a nie prowadzić spór proceduralny sam ze sobą. Pytanie do operatora jest potrzebne tylko wtedy, gdy brak decyzji rzeczywiście zmienia wynik lub zakres.

## 3. Stan projektu

Repozytorium jest jedynym źródłem stanu projektu.

- GitHub i gałąź `master` przechowują przyjętą wersję główną.
- Lokalna kopia na dysku C jest warsztatem roboczym Codexa.
- Backup archiwalny jest kopią bezpieczeństwa, nie równoległym źródłem prawdy.
- Pamięć modelu, rozmowa ani ZIP nie zastępują zapisu w repozytorium.

Przed zmianą należy sprawdzić aktualny stan repozytorium. Nie wymaga to osobnego rytuału, jeżeli stan można potwierdzić bezpośrednio narzędziami.

## 4. Bramki proporcjonalne do ryzyka

Anonimizacja, formalny audyt, niezależna recenzja, rozbudowany pakiet przekazania, specjalistyczny interfejs lub dodatkowy model nie są domyślną bramką pracy warsztatowej.

Uruchamia się je, gdy:

- produkt jest gotowy lub stabilny i ma wyjść poza prywatny warsztat;
- materiał ma zostać udostępniony zewnętrznie;
- zadanie dotyczy danych osób trzecich, bezpieczeństwa, prawa, zdrowia lub innego realnego ryzyka;
- koszt błędu uzasadnia dodatkową kontrolę;
- operator zażąda jej wprost.

Bramka ma odpowiadać konkretnemu ryzyku i nie może automatycznie rozrastać się na cały proces.

## 5. Tryb wynikający z polecenia

- `oceń`, `sprawdź`, `zaproponuj` oznaczają odpowiedź bez zmiany plików;
- `zrób`, `napisz`, `wygeneruj`, `zaktualizuj` oznaczają wykonanie i zapis w uzgodnionym zakresie;
- polecenie jednoznaczne i odwracalne wykonuje się bez dodatkowego potwierdzenia;
- dodatkowe potwierdzenie jest wymagane przed działaniem zewnętrznym, kosztownym, nieodwracalnym albo wykraczającym poza podany zakres.

## 6. Kryterium zakończenia

Zadanie jest zakończone, gdy uzgodniony rezultat istnieje, został sprawdzony proporcjonalnie do ryzyka, stan repozytorium jest czytelny, a operator otrzymał krótkie podsumowanie.

Nie tworzy się dodatkowych raportów, rejestrów ani interfejsów, jeżeli nie są potrzebne do wykonania lub sprawdzenia zadania.
