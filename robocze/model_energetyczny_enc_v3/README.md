# Model energetyczny E–N–C v3 — zachowany rdzeń roboczy

Status produkcyjny: materiał roboczy  
Status epistemiczny: hipoteza formalna bez kalibracji empirycznej  
Pochodzenie: gałąź `agent/model-energetyczny-errata-szew`

## Zachowana treść

- `robocze/MODEL_ENERGETYCZNY_SCALENIE_I_ERRATY_v0.2.md` — rama pojęciowa, granice i kryteria domknięcia;
- `narzedzia/model_energetyczny_enc_v3/rdzen.py` — równania i podstawowe struktury modelu;
- `narzedzia/model_energetyczny_enc_v3/przebieg.py` — przebiegi symulacyjne;
- `narzedzia/model_energetyczny_enc_v3/rownowagi.py` — analiza punktów równowagi.

Nie przeniesiono transportowych części ZIP, skryptu odtwarzania paczki, handoffów ani mandatów audytowych. Nie są potrzebne do odczytu zachowanego rdzenia.

## Granice

Model nie jest skalibrowany na danych ludzkich. Wartości `E`, `N`, `C`, `K` i `Omega` nie są diagnozą ani pomiarem człowieka. Progi uzyskane w symulacji opisują wyłącznie badaną parametryzację.

Kod wymaga Pythona oraz biblioteki NumPy. Pliki pozostają materiałem warsztatowym do dalszej ręcznej oceny.
