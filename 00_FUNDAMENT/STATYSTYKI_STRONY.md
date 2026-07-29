# Statystyki strony INFINITA

## Źródło prawdy

Google Analytics 4 jest źródłem statystyk publicznej strony INFINITA.

Aktualny raport maszynowy znajduje się w:

`dane_publiczne/statystyki_strony.json`

Na pytanie o statystyki strony model najpierw czyta ten plik. Nie rozpoczyna ponownego projektowania analityki i nie opiera odpowiedzi na pamięci poprzedniego czatu.

## Zakres raportu

Raport obejmuje:

- użytkowników;
- nowych użytkowników;
- użytkowników nowych i powracających;
- sesje;
- odsłony;
- średni czas sesji;
- wskaźnik zaangażowania;
- źródła wejścia;
- najczęściej odwiedzane strony;
- kraje;
- urządzenia;
- okres raportu i datę aktualizacji.

## Automatyzacja

Workflow `.github/workflows/statystyki-ga4.yml` pobiera dane codziennie oraz na żądanie przez Google Analytics Data API i zapisuje wynik w repozytorium.

Wymagane sekrety repozytorium:

- `GA4_PROPERTY_ID`;
- `GA4_SERVICE_ACCOUNT_JSON`.

Konto serwisowe Google musi mieć wyłącznie uprawnienie odczytu do właściwości GA4.

## Prywatność

Kod analityczny strony ma działać zgodnie ze zgodą wyrażoną w banerze cookies.

Ruch operatora należy oznaczyć w GA4 jako ruch wewnętrzny i wykluczyć z raportów. Repozytorium nie przechowuje surowych adresów IP ani danych identyfikujących odwiedzających.

## Kontrola aktualności

Jeżeli `status` w pliku raportu ma wartość `NIEPODLACZONE`, statystyki nie są jeszcze dostępne. Jeżeli raport ma starą datę `generated_at`, odpowiedź musi wskazać, że automatyzacja wymaga kontroli.
