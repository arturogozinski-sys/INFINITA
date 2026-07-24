# Archiwum źródłowe modelu ENC v3

Ten katalog przechowuje dokładny ZIP otrzymany od Claude’a 2026-07-24, zakodowany jako osiem części Base64.

## Odtworzenie

Z katalogu głównego repozytorium:

```bash
python narzedzia/model_energetyczny_enc_v3/odtworz_paczke.py --cel /tmp/model_enc_v3 --zachowaj-zip
```

Skrypt zatrzymuje działanie przy brakującej części, błędnym Base64, niezgodnej zawartości ZIP-a lub różnicy SHA-256.

## Sumy kontrolne

```text
0f711f8052471a10385709a532e1b10a97c5cb43761916c6497570ebbf3315f2  połączony tekst Base64
558c05999563b30429adad92709fe2c5680dd1cbe6e78a9c2404ab8ff058f52c  model_enc_v3.zip
```

Autorytatywna jest paczka odtworzona i zweryfikowana przez skrypt. Pojedyncze kopie kodu w `narzedzia/model_energetyczny_enc_v3/` służą wyłącznie do wygodnego przeglądu.
