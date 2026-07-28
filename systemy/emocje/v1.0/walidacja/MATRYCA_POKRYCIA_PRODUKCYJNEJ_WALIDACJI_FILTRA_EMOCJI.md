MATRYCA POKRYCIA WEWNĘTRZNEJ WALIDACJI STRUKTURALNEJ FILTRA EMOCJI

Status dokumentu: zamknięty zapis pokrycia

Jednostka pokrycia

Jednostką nie jest dowolna kombinacja słownika, lecz odrębna ścieżka wykonania reguły. Powtórzenie tej samej ścieżki innymi słowami nie zwiększa pokrycia strukturalnego.

Synteza kandydatów

Pokrywa się poprawne włączenie każdej rodziny.

Pokrywa się osobno niespełnienie każdego warunku koniecznego każdej rodziny.

Pokrywa się osobno każdą wartość występującą w alternatywie.

Pokrywa się wartość nieokreśloną w każdym wymiarze używanym przez reguły włączania.

Pokrywa się zbiór zawierający wartość zgodną i niezgodną w każdym wymiarze używanym przez reguły włączania.

Pokrywa się zbiór zawierający wyłącznie wartości niespełniające warunku.

Test działania

Dla każdej rodziny pokrywa się działanie zgodne.

Dla każdej rodziny pokrywa się działanie sprzeczne.

Dla każdej rodziny pokrywa się działanie nieokreślone.

Dla każdej rodziny pokrywa się zbiór działań zawierający kierunek zgodny i niezgodny.

Test domknięcia

Dla każdej rodziny pokrywa się zgodne wygasanie.

Dla każdej rodziny pokrywa się zgodne utrwalanie.

Dla każdej rodziny pokrywa się domknięcie nieokreślone.

Dla każdej rodziny pokrywa się wygasanie połączone z warunkiem utrwalania.

Dla każdej rodziny pokrywa się utrwalanie połączone z warunkiem wygasania.

Wynik końcowy

Pokrywa się pojedynczego kandydata dla każdej rodziny.

Pokrywa się każdą parę rodzin jako próbę współwystępowania kandydatów.

Pokrywa się konflikty obejmujące więcej niż dwie rodziny.

Pokrywa się brak kandydata po syntezie.

Pokrywa się brak kandydata po teście działania.

Pokrywa się brak kandydata po teście domknięcia.

Kryterium zakończenia

Walidacja strukturalna jest kompletna dopiero wtedy, gdy każda jednostka pokrycia posiada zamknięty rekord, zamknięty klucz oraz dwie utrwalone oceny.

Brak możliwości zbudowania sensownego rekordu dla jednostki pokrycia zostaje zapisany jako granica słownika albo reguły. Nie zastępuje się go przypadkiem z innej ścieżki.

Wynik pokrycia

Każda jednostka pokrycia posiada zamknięty rekord, zamknięty klucz oraz dwie utrwalone oceny.

Poprawne włączenia, niespełnienie warunków koniecznych i gałęzie alternatyw pokryły serie pierwsza i druga.

Wartości nieokreślone, zbiory zawierające wartość zgodną i niezgodną oraz zbiory zawierające wyłącznie wartości niespełniające warunku pokryła seria trzecia. Trzy niemożliwe konstrukcje zapisano jako granice słownika.

Test działania pokryła seria czwarta.

Test domknięcia pokryła seria piąta.

Wszystkie pary rodzin i konflikty wielorodzinne pokryła seria szósta.

Brak kandydata po syntezie, teście działania i teście domknięcia posiada zamknięte przypadki w seriach drugiej, trzeciej, czwartej i piątej.

Pokrycie strukturalne zamrożonego filtra jest kompletne.
