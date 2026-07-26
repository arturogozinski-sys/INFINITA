# PRZEPŁYW PRACY AI W INFINITA

## Cel

Zapewnić Arturowi prostą pracę w jednym środowisku bez ręcznego transportu kontekstu i wielomodelowej biurokracji.

## Układ podstawowy

1. Artur określa cel albo korektę.
2. ChatGPT/Codex sprawdza lokalny stan repozytorium.
3. Codex wykonuje zmianę, używając agentów pomocniczych tylko wtedy, gdy realnie upraszczają pracę.
4. Codex uruchamia testy lub inne kontrole adekwatne do zmiany.
5. Artur recenzuje wynik i podejmuje ostateczną decyzję.
6. Przyjęty stan trafia do `master` na GitHubie.

Nie ma obowiązku przekazywania pracy między różnymi markami modeli, tworzenia pakietów handoff ani uzyskiwania akceptacji niezależnego modelu.

## Stan i kopie

- GitHub `arturogozinski-sys/INFINITA`, gałąź `master`: wersja główna.
- Lokalna kopia na dysku C: bieżący warsztat.
- Backup archiwalny: okresowa kopia bezpieczeństwa poza repozytorium.

ZIP, rozmowa i pamięć modelu nie są źródłem prawdy.

## Kontrola proporcjonalna

W prototypach oraz testach mechanicznych i wdrożeniowych wystarczają kontrole potrzebne do potwierdzenia działania. Formalne audyty, anonimizacja, specjalistyczne interfejsy, dodatkowi recenzenci i rozbudowane procedury wchodzą dopiero przy stabilnym lub gotowym produkcie, udostępnianiu materiału na zewnątrz albo realnie wysokim koszcie błędu.

Bezpieczeństwo, prawo, zdrowie i dane osób trzecich nadal wymagają reakcji adekwatnej do rzeczywistego ryzyka.

## Kryterium zakończenia

Rezultat istnieje, potrzebne kontrole przeszły, zmienione pliki i stan Git są czytelne, a Artur otrzymał krótkie podsumowanie. Czyste drzewo robocze, pull request, CI, formalny raport lub niezależna recenzja są wymagane tylko wtedy, gdy wynikają z konkretnego zadania.
