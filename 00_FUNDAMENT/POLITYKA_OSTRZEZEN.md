# Polityka ostrzeżeń

Ostrzeżenie jest otwartą decyzją, a nie stałym tłem raportu. Każde ostrzeżenie objęte automatyczną kontrolą ma datę pierwszego sygnału, kategorię, właściciela rozstrzygnięcia i termin.

Po terminie ostrzeżenie wskazane przez politykę staje się blokerem CI. Zamknięcie wymaga usunięcia przyczyny albo jawnej zmiany klasy i terminu wraz z podstawą; samo przepisanie daty nie jest rozstrzygnięciem.

Pierwszym wdrożonym zakresem są martwe odwołania. Ich rejestr i terminy znajdują się w `KLASYFIKACJA_MARTWYCH_ODWOLAN.json`, a egzekwowanie wykonuje `narzedzia/generuj_raport_martwych_odwolan.py`. Pozostałe kategorie nie eskalują automatycznie, dopóki nie otrzymają równie jednoznacznego rejestru.

Stan `nierozstrzygniete` nie jest piątą klasą odwołania. Oznacza wyłącznie brak danych potrzebnych do wyboru jednej z czterech klas i ma krótki termin na decyzję.
