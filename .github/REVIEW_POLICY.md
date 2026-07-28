# Zasady przeglądu zmian

Każda zmiana głównej gałęzi przechodzi przez pull request.

Warunki scalenia:

1. CI zakończyło się powodzeniem.
2. Zmiana osoby spoza właścicieli kodu wymaga przeglądu i decyzji Operatora.
3. Nowy commit po przeglądzie wymaga ponownej kontroli zmienionego zakresu.
4. Wszystkie rozmowy przeglądu są rozwiązane.
5. Gałąź pull requestu jest aktualna względem głównej gałęzi.

Nie wolno wykonywać force-push ani usuwać głównej gałęzi. Reguły obowiązują
również administratora repozytorium. Kierunek projektu i decyzja o scaleniu
pozostają pod kontrolą Operatora.

Techniczny wymóg co najmniej jednej akceptacji zostanie włączony po dodaniu
zaufanego recenzenta. GitHub nie pozwala autorowi zatwierdzić własnego pull
requestu, więc wcześniejsze włączenie tej bramki zablokowałoby repozytorium
prowadzone przez jednego właściciela.
