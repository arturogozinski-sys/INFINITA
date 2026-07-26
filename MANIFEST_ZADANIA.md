# MANIFEST ZADANIA — OPCJONALNY

Manifest nie jest bramką wejściową dla zwykłej pracy w ChatGPT/Codex.

Stosuje się go tylko wtedy, gdy:

- zadanie jest formalnym audytem;
- obejmuje duży lub kosztowny pakiet zmian;
- wymaga przekazania pracy na zewnątrz;
- koszt pomyłki uzasadnia zamrożenie zakresu i stanu wejściowego;
- operator zażąda manifestu.

W pozostałych przypadkach wystarczają: cel operatora, aktualny stan repozytorium, zakres wynikający z zadania, adekwatne sprawdzenie oraz krótkie podsumowanie.

## Minimalny manifest, gdy jest potrzebny

```yaml
repozytorium: arturogozinski-sys/INFINITA
commit_bazowy: <SHA>
cel: <JEDNO ZDANIE>
zakres:
  - <PLIK LUB OBSZAR>
kryterium_zakonczenia: <SPRAWDZALNY WYNIK>
ryzyko_wymagajace_bramki: <OPIS>
decyzje_operatora: []
```

Manifest nie może służyć do zatrzymywania jednoznacznej, odwracalnej pracy ani tworzyć obowiązku ręcznego kopiowania stanu, który Codex może odczytać z repozytorium.
