# Model energetyczny E–N–C v3 — zabezpieczony snapshot roboczy

Status produkcyjny: materiał roboczy, zabezpieczony snapshot  
Status epistemiczny: hipoteza formalna po audycie, bez kalibracji empirycznej  
Pochodzenie: paczka Claude przekazana 2026-07-24 jako `files(3).zip`  
Bazowy stan repo przy imporcie: `master@52ad34623dc801103b63f5e3adb0d56257008905`

## Cel zapisu

Zabezpieczenie dokładnego stanu modelu po korektach dotyczących:

- semantyki `E=0`;
- rozdzielenia strumienia `K` od stanów `E`, `N`, `C`;
- niezmienniczości dziedziny;
- usunięcia `E_0` i `C_min` z rdzenia;
- wprowadzenia bazowej regeneracji `r_0`;
- analizy punktów stałych;
- wykrycia dwóch punktów siodło–węzeł;
- bistabilności i histerezy obecnej parametryzacji;
- poprawienia aktualizacji śladów `S_minus` i `S_plus` do jednego kroku na iterację;
- wycofania przenoszenia statycznego `K=const` na wymuszenie okresowe `K(t)`.

## Autorytatywny artefakt snapshotu

Dokładna paczka źródłowa jest przechowywana bajt w bajt jako osiem części Base64:

`robocze/model_energetyczny_enc_v3/paczka/model_enc_v3.zip.b64.part-00` … `part-07`

Odtworzenie i kontrolę wykonuje:

```bash
python narzedzia/model_energetyczny_enc_v3/odtworz_paczke.py --cel /tmp/model_enc_v3
```

Skrypt sprawdza:

1. komplet i kolejność ośmiu części;
2. SHA-256 połączonego tekstu Base64;
3. SHA-256 odtworzonego ZIP-a;
4. dokładny zestaw sześciu plików w ZIP-ie;
5. SHA-256 każdego wypakowanego pliku.

### Sumy archiwum

```text
0f711f8052471a10385709a532e1b10a97c5cb43761916c6497570ebbf3315f2  połączony tekst Base64
558c05999563b30429adad92709fe2c5680dd1cbe6e78a9c2404ab8ff058f52c  model_enc_v3.zip
```

## Pliki wygodne do przeglądu

W repo bezpośrednio zapisano także trzy pliki najważniejsze dla szybkiego code review:

- `narzedzia/model_energetyczny_enc_v3/rdzen.py`
- `narzedzia/model_energetyczny_enc_v3/przebieg.py`
- `narzedzia/model_energetyczny_enc_v3/rownowagi.py`

Pełna, rozstrzygająca zawartość, obejmująca również `dobowy.py`, raport i wynik referencyjny, pochodzi zawsze z odtworzonego archiwum. Pliki wygodne nie zastępują archiwum.

## Granice twierdzeń

Nie wolno na podstawie tego snapshotu twierdzić, że:

1. parametry są skalibrowane na danych ludzkich;
2. progi `K≈0,125795` i `K≈0,326309` są progami człowieka;
3. trzy zmienne są empirycznie wystarczające;
4. `E=0` oznacza biologiczne wyczerpanie albo rozstrzyga zachowanie zewnętrzne;
5. wyniki dla stałego `K` dowodzą zachowania przy okresowym `K(t)`;
6. model może sterować interakcją z operatorem bez osobnej walidacji funkcjonalnej;
7. wartości `E`, `N`, `C` albo `Omega` powinny być pokazywane operatorowi jako diagnoza.

## Wynik walidacji przy imporcie

- źródłowe archiwum zawierało 6 plików;
- wszystkie 4 źródłowe pliki Python przeszły lokalnie `python -m py_compile` przed importem;
- pełne uruchomienie `dobowy.py` nie jest deklarowane w tym commicie jako ponownie wykonane;
- `PRZEBIEG_PELNY.txt` jest artefaktem referencyjnym z paczki Claude’a;
- pełna reprodukcja, kontrola sum i porównanie stdout bajt w bajt pozostają obowiązkiem Copilota/CI.

## SHA-256 plików wewnątrz paczki

```text
5c0b7ca3808d21032ef330f0b2920a704fe6a66d73eb912bae56d8ceddfdc48d  rdzen.py
141572c86a6e9b21f179e3ee8b0952e21ffc70c42b87d7a3ae58bdd36b024ca1  przebieg.py
5a587ab3411aa09a46321a645cfb97ccfe0d6fd7fcbc126cd2535f8d212e5f6c  rownowagi.py
5935a6ce6f5792e17f9b0d6978d10a514ee8a89b4c1505e103741579e7e81841  dobowy.py
bc52baa1338b8d563082c907e693039434828f16374059fe854df63d0c78a927  RAPORT_E0_KUMULACJA_v3.md
e95686f59a3a9590052c4e5447a7b66b944304dee123b8a260eb8a45c5a9b359  PRZEBIEG_PELNY.txt
```

## Relacja do PR #13

Snapshot rozszerza dokument scalenia i erraty v0.2 o wykonawczy stan v3. Nie zastępuje kanonu, nie zmienia dokumentów nadrzędnych i nie jest przeznaczony do automatycznego scalenia bez niezależnej recenzji.
