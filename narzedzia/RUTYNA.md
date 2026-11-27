# Rutyna nocna: materiały dla kursantów indywidualnych

Procedura, którą Claude wykonuje codziennie o 00:00 (Europe/Oslo). Materiały publikuje bez sprawdzania przez lektorkę.
Narzędzia: Google Drive (connector), repo `norskling/cwiczenia` (ten katalog), Python z `python-pptx`.

## 0. Stałe

- Shared drive „Automatyczne materiały”, folder **Kursanci indywidualni**: `1QO0JccYarRyCCEx76uD37k5yzI90anhk`
- Folder **Feedback lektorek** (baza zasad od lektorek): `1zXGjNNPxGWc6zUErT4dtp_gw_7cd80i4` (w katalogu głównym shared drive)
- Folder **Raporty rutyny** (raport z każdego przebiegu): `1Ij4U5MD2norAN4IRNA7i0JxieoaKEoa-` (w katalogu głównym shared drive)
- Strony online: `https://norskling.github.io/cwiczenia/c/<slug>.html`
- Wzorzec jakości (A2, Marta Przykładowa): `narzedzia/przyklady/*.json`, prezentacja Slides `1zpSR6Mgqh2Jfz_B0lNg8NPtm3zA-onQPCMKLIqLBZaM`
- Styl: skill `norskling-new-brand` (jasne tło, granatowe nagłówki Space Grotesk, niebieskie podkreślenie, białe karty). Generatory mają ten styl wbudowany.

## 1. Znajdź kursantów

1. `search_files` z `parentId = '<Kursanci indywidualni>'`, tylko foldery. Pomiń folder **Wzór** (chyba że uruchomienie testowe mówi inaczej).
2. W folderze kursanta znajdź **Folder lektorki** (dokument „Notatki: …” + podfoldery „Lekcja M” z materiałami PRZED lekcją) i **Folder kursanta** (podfoldery „Lekcja N” ze zrzutami ekranu i dokumentem PO lekcji).

**Gdzie co trafia (Monika, 2026-11-20):** prezentacja i dokument „Lekcja M: materiały na lekcję” → `Folder lektorki / Lekcja M`. Dokument „Lekcja N: słownictwo i zadania” → `Folder kursanta / Lekcja N`. Nic innego nie trafia do folderu kursanta.
3. Brak dokumentu notatek albo brak któregoś folderu: zapisz w raporcie, przejdź do następnego kursanta.

## 1a. Wczytaj bazę feedbacku lektorek (zawsze, przed kursantami)

1. `search_files` z `parentId = '1zXGjNNPxGWc6zUErT4dtp_gw_7cd80i4'`, tylko dokumenty z nazwą zaczynającą się od „Feedback” (pomiń „_Jak działa baza feedbacku”). Każdy przeczytaj `read_file_content`.
2. Każdy wpis ma pola: DATA, LEKTORKA, DOTYCZY, MATERIAŁ, CO BYŁO NIE TAK, ZASADA, STATUS. Pomiń wpisy ze STATUS = NIEAKTUALNA.
3. DOTYCZY = OGÓLNE → stosuj ZASADĘ we wszystkich materiałach (w zakresie pola MATERIAŁ). DOTYCZY = imię kursanta lub nazwa grupy → stosuj tylko u niego/niej.
4. Kolejność ważności: notatki lektorki z bieżącej lekcji > nowszy wpis feedbacku > starszy wpis > domyślne zasady z tej procedury.
5. Zasady stosuj przy pisaniu specyfikacji JSON (ćwiczenia, drill, prezentacja, zadanie domowe), zanim uruchomisz generatory. Nie przerabiaj materiałów, które już powstały.
6. W raporcie przy każdym kursancie wypisz, które wpisy feedbacku zastosowałeś (nazwa dokumentu). Wpis niejasny albo sprzeczny z notatkami: zapisz to w raporcie.
7. Treści feedbacku nie kopiuj do repo (repo jest publiczne).

## 1b. Stałe zasady jakości (feedback lektorek, obowiązują zawsze)

Zasady z feedbacku lektorek przeniesione na stałe do procedury. Obowiązują u wszystkich kursantów, także gdy baza na Drive jest pusta.

1. **Bez personalnych wstawek.** Nie komentuj, że materiał jest o zainteresowaniach kursanta (źle: „Wioletta, ten zestaw jest o rzeczach, które lubisz: koty, robienie na drutach…”). Zainteresowania i profil wplataj w treść zdań, bez mówienia o tym. Wstępy do zestawów bez zwracania się po imieniu. (2026-11-27)
2. **Bez podpowiedzi gramatycznych w poleceniach od A2 wzwyż.** Polecenie nie mówi, jaki rodzaj ma słowo, w jakiej formie (określona/nieokreślona, liczba, czas) je wpisać itp. Kursant ma to wiedzieć sam. Na A1 wolno, oszczędnie. Wyjaśnienie „dlaczego” należy do przycisku podpowiedzi (`why`) po odpowiedzi, nie do polecenia. (2026-11-27)
3. **Zadania nie za banalne.** Trudność dopasuj do poziomu: unikaj zadań rozwiązywalnych bez znajomości tematu lekcji, zgadywanych z kontekstu albo z jedną oczywistą odpowiedzią. Od B1 przewaga zadań, w których kursant sam tworzy formę (wpisywanie, przekształcanie, układanie zdań), nad prostym wyborem. (2026-11-27)
4. **Reguły gramatyczne muszą być prawdziwe.** Nie upraszczaj reguły tak, że staje się fałszywa. Źle: „„en” razem z końcówką -en nigdy nie występuje” (są *en morgen*, *en eksamen*). Dobrze: „Nie łączymy rodzajnika nieokreślonego z formą określoną: *en bil* albo *bilen*, nigdy *en bilen*.” Przed wpisaniem reguły do polecenia, podpowiedzi albo slajdu sprawdź, czy nie ma oczywistych wyjątków; jeśli są, sformułuj ją węziej albo pomiń. (2026-11-27)

Nowe stałe zasady dopisuje tu Claude, gdy Monika przekaże feedback lektorki. Bieżący feedback lektorek z Drive (sekcja 1a) uzupełnia te zasady.

## 2. Odczytaj notatki (`read_file_content`)

Tabele mają 2 kolumny: etykieta WIELKIMI LITERAMI z dwukropkiem, wartość po prawej. Zaznaczenie = `[X]` lub `[x]`, puste = `[ ]`
(w eksporcie nawiasy są poprzedzone ukośnikami, ignoruj je).

Strona 1:
- **STATUS KURSU**: `ZAKOŃCZONY` zaznaczony → pomiń kursanta.
- **PAKIET GODZIN**: zaznaczona liczba albo liczba wpisana po `INNY:` (np. `_24___` → 24).
- **WYKORZYSTANE GODZINY**: liczba. Jeśli ≥ pakiet → nie twórz nic, zapisz w raporcie „pakiet wykorzystany”.
- **IMIĘ**, **POZIOM**, profil (KIM JEST, PRACA, CEL NAUKI, HOBBY, RODZINA, INNE UWAGI).
- „Plan materiałów na lekcję 1” + **GOTOWE DO GENEROWANIA** (dotyczy lekcji 1).

Strona **LEKCJA N** (każda kolejna): notatki z lekcji N, „Plan materiałów na lekcję N+1”, „Zadanie domowe po lekcji N”,
**GOTOWE DO GENEROWANIA** (dotyczy całej strony).

Pole puste albo z tekstem szablonu (np. „[Imię Nazwisko]”) traktuj jako brak danych. Nie zgaduj danych, których nie ma.

## 3. Ustal kroki do wykonania

Krok jest **zrobiony**, gdy istnieje dokument o dokładnej nazwie z kroku: dla PRZED w `Folder lektorki / Lekcja M` **albo** (materiały sprzed 2026-11-20) w `Folder kursanta / Lekcja M`; dla PO w `Folder kursanta / Lekcja N`. Nie powtarzaj zrobionych kroków i nie przenoś starych plików.

| Krok | Warunek | Źródło planu | Wynik |
|---|---|---|---|
| **PRZED lekcją M** | strona źródłowa ma GOTOWE `[X]` | M=1: strona 1; M>1: strona LEKCJA M-1 | `Folder lektorki / Lekcja M`: „Lekcja M: materiały na lekcję” (+ prezentacja, jeśli zaznaczona) |
| **PO lekcji N** | strona LEKCJA N ma GOTOWE `[X]` | strona LEKCJA N + zrzuty ekranu | `Folder kursanta / Lekcja N`: „Lekcja N: słownictwo i zadania” |

Kolejność dla jednej strony LEKCJA N: najpierw PO lekcji N, potem PRZED lekcją N+1. Brakujący folder „Lekcja K” utwórz
(`create_file`, mimeType folder, parent = Folder lektorki dla kroku PRZED, Folder kursanta dla kroku PO).

## 4. Krok PRZED lekcją M

Czytaj plan: DŁUGOŚĆ LEKCJI, PREZENTACJA (TAK/NIE), TEMAT, ZAKRES GRAMATYCZNY, ĆWICZENIA GRAMATYCZNE (+czas, zakres),
ĆWICZENIA ZE SŁOWNICTWA (+czas, temat), MUNTLIG DRILL (+czas, tematy), FORMA ĆWICZEŃ, DODATKOWE UWAGI.
Uwzględnij też notatki z poprzedniej lekcji (NAJWIĘKSZY PROBLEM, OPIS PROBLEMU, CO POTRZEBNE): problemy z poprzedniej lekcji wracają w ćwiczeniach jako powtórka.

Zasady treści:
- Poziom zgodny z POZIOM. Zdania przykładowe budowane z profilu: praca, rodzina, hobby, miejsce zamieszkania. Kelnerka dostaje zdania z restauracji, opiekunka zdania ze zmiany i mieszkańców.
- Na stronach online tylko imię. Bez nazwiska, e-maila, nazwy pracodawcy, nazwiska lektorki i treści notatek lektorki.
- Polecenia po polsku, przykłady po norwesku (bokmål). Sprawdź poprawność norweskiego, w tym rodzaj i odmianę.
- FORMA: „dużo krótkich” → wiele pojedynczych zadań; „kilka dłuższych” → mniej zadań, więcej tekstu/przekształceń.

### 4a. Ćwiczenia (gdy GRAMATYCZNE lub SŁOWNICTWO = TAK)
Jedna strona z częściami. Ok. 1,3 zadania na minutę (20 min → ok. 25 zadań). Spec jak `przyklady/a2_cwiczenia.json`.
```
cd narzedzia && S=$(python3 pomocnicze.py slug) && python3 generuj_cwiczenia.py /tmp/rutyna/<imie>_L<M>_cw.json ../c/$S.html
```

### 4b. Muntlig drill (gdy MUNTLIG DRILL = TAK)
Ok. 1 karta na 2,5 min (10 min → 4 karty, 20 min → 8). Każda karta: pytanie, tłumaczenie, 6–9 słów kluczowych, 3–4 pytania pomocnicze.
Spec jak `przyklady/a2_drill.json`. `python3 generuj_drill.py spec.json ../c/$S.html`.

### 4c. Prezentacja (TYLKO gdy PREZENTACJA = `[X] TAK`)
Spec JSON dla `generuj_prezentacje.py` (typy slajdów w nagłówku skryptu). Struktura: tytul, plan, potem na zmianę slajd teorii i slajd rozmowy
(skrypt odrzuca dwa slajdy teorii bez rozmowy pomiędzy), na końcu podsumowanie. 90 min → ok. 14–18 slajdów, 45 min → ok. 9–12.
```
python3 generuj_prezentacje.py spec.json ../L<M>.pptx
```
Plik .pptx zapisz w katalogu roboczym sesji (korzeń repo, `*.pptx` jest w `.gitignore`). Referencja `sha256:` działa tylko dla plików w katalogu roboczym, z `/tmp` wgranie się nie uda.
Wgranie: `create_file` z `parentId` = `Folder lektorki / Lekcja M`, `title` „Lekcja M: prezentacja (<temat>)”,
`contentMimeType` `application/vnd.openxmlformats-officedocument.presentationml.presentation`,
`base64Content` = referencja `sha256:<sha256 pliku>:<ścieżka absolutna>` (sha256 policz `sha256sum`) (bez `disableConversionToGoogleType`, plik ma się przekonwertować do Slides).
Sprawdź wynik `read_file_content` (liczba slajdów). Gdy wgranie się nie uda, i tak opublikuj resztę i zapisz błąd w raporcie.

### 4d. Publikacja stron
```
cd <repo> && git checkout main && git pull --rebase origin main
git add c/ && git commit -m "Materiały: <Imię> lekcja <M>" && git push origin HEAD:main
```
Monika pozwoliła publikować prosto na `main` (bez PR). Push ponawiaj do 4 razy przy błędzie sieci.

### 4e. Dokument „Lekcja M: materiały na lekcję”
Spec dla `pomocnicze.py dokument` z jedną sekcją `links` (prezentacja, muntlig drill, ćwiczenia; w opisie liczba slajdów/pytań/zadań i czas).
Wgranie: `create_file`, `parentId` = `Folder lektorki / Lekcja M`, `title` dokładnie „Lekcja M: materiały na lekcję”, `textContent` = HTML, `contentMimeType` `text/html`.
Ten dokument tworzysz NA KOŃCU kroku, bo jego istnienie oznacza „zrobione”.

## 5. Krok PO lekcji N

1. Zrzuty ekranu: pliki graficzne w `Folder kursanta / Lekcja N` oraz w `Folder lektorki / Lekcja N`, jeśli tam są (`mimeType contains 'image/'`). Każdy przeczytaj (`read_file_content`), zwróć uwagę na dopiski lektorki.
   Gdy ZRZUTY EKRANU WGRANE = TAK, a plików nie ma, zbuduj słownictwo z notatek i zapisz to w raporcie.
2. Słownictwo: tabela Norsk / Polski / Przykład (przykład z profilu kursanta), 8–20 pozycji, tylko słowa, które były na lekcji.
3. Zadanie domowe (gdy ZADANIE DOMOWE = TAK): wg INSTRUKCJI. Część do zrobienia online publikujesz jako osobną stronę ćwiczeń
   (lub linkujesz istniejące ćwiczenia z lekcji, gdy instrukcja tak mówi). Część pisemną/ustną opisz jako krok listy. Czas wg CZAS ZADANIA DOMOWEGO.
4. Dokument „Lekcja N: słownictwo i zadania” w `Folder kursanta / Lekcja N`: sekcja `table` (słownictwo) + sekcja `steps` (zadanie domowe z linkami). Tworzysz go na końcu.

## 6. Raport

Na koniec przebiegu utwórz w folderze **Raporty rutyny** dokument „Raport rutyny RRRR-MM-DD” (tylko gdy coś powstało albo wystąpił problem):
dla każdego kursanta: co powstało (linki), zastosowane wpisy feedbacku, co pominięto i dlaczego (np. brak GOTOWE, pakiet wykorzystany, brak zrzutów, błąd wgrania).
Bez danych kontaktowych kursantów.

## 7. Czego nie robić

- Nie zmieniaj dokumentów notatek (brak uprawnień i tak nie pozwala).
- Nie twórz materiałów PO lekcji przed lekcją (bez GOTOWE na stronie LEKCJA N nic nie powstaje).
- Nie twórz prezentacji, gdy nie jest zaznaczona.
- Nie publikuj nazwisk ani notatek lektorki w repo (repo jest publiczne). Specyfikacje JSON trzymaj w /tmp, nie w repo.
