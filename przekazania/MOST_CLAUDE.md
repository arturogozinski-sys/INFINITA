# MOST PRACY CLAUDE ↔ GITHUB

## Cel

Zapewnić Claude’owi potwierdzony, wersjonowany stan repozytorium bez udawania bezpośredniego dostępu do GitHuba.

## Zasada źródła prawdy

- `master` na GitHubie jest jedynym źródłem prawdy.
- ZIP jest wyłącznie snapshotem transportowym.
- Każdy snapshot zawiera `CLAUDE_SNAPSHOT.yaml` z pełnym `commit_bazowy`.
- Claude nie może zakładać, że snapshot jest aktualny względem GitHuba.

## Przepływ wejściowy

1. Po scaleniu istotnej zmiany workflow `Claude snapshot` uruchamia testy.
2. Snapshot powstaje wyłącznie, gdy testy przejdą.
3. GitHub Actions publikuje artefakt `infinita-claude-<SHA>` na 14 dni.
4. Artefakt jest pobierany i przekazywany Claude’owi jako jedyny stan roboczy.
5. Claude przed rozpoczęciem pracy odczytuje `CLAUDE_SNAPSHOT.yaml`.

## Przepływ wyjściowy

Claude zwraca:

- zmienione pliki albo pełny snapshot wyniku,
- `HANDOFF.yaml`,
- pełny `commit_bazowy`,
- listę zmienionych plików,
- uruchomione testy i ich wynik,
- ograniczenia i decyzje wymagane od operatora.

## Bramka importu

Materiał Claude’a może trafić do gałęzi roboczej tylko wtedy, gdy:

- `commit_bazowy` istnieje w repo,
- różnice względem aktualnego `master` są jawne,
- import nie nadpisuje nowszego stanu bez porównania,
- testy przechodzą,
- drzewo po testach pozostaje czyste.

Rozjazd SHA zatrzymuje automatyczny import. Nie jest naprawiany przez zgadywanie ani przez ręczne łączenie treści bez raportu różnicowego.

## Recenzja

1. Zmiany trafiają do draft PR.
2. CI uruchamia testy i czujniki integralności.
3. Copilot przegląda diff.
4. GPT i operator oceniają sens merytoryczny, ryzyko oraz zgodność z fundamentem.
5. Scalenie do `master` wymaga decyzji operatora.

## Granice

Most nie daje Claude’owi ciągłego dostępu do GitHuba. Zapewnia mu potwierdzony snapshot i jednoznaczną drogę zwrotną. Automatyzacja techniczna nie obejmuje samodzielnego zmieniania kanonu ani statusów epistemicznych.
