# Narzędzia do generowania materiałów

Skrypty, z których Claude korzysta przy tworzeniu ćwiczeń dla kursantów indywidualnych.

- `generuj_cwiczenia.py spec.json c/<slug>.html`: interaktywne ćwiczenia (wybór, uzupełnianie, przekształcanie, dopasowanie, tekst).
- `generuj_prezentacje.py spec.json wynik.pptx`: prezentacja z JSON (slajdy teorii przeplatane slajdami rozmowy).
- `pomocnicze.py slug` / `pomocnicze.py dokument`: losowy slug i HTML dokumentu na Drive.
- `RUTYNA.md`: pełna procedura nocnej rutyny.
- `generuj_drill.py spec.json c/<slug>.html`: muntlig drill jako quiz: jedno pytanie na ekranie, przycisk „Następne pytanie”, osobne przyciski „Słowa kluczowe” i „Pytania pomocnicze” (oppfølgingsspørsmål), stoper 2 lub 4 min, strzałki ← → na klawiaturze.
- `styl.css`, `skrypt.js`: wspólny styl Norskling i logika sprawdzania.
- `przyklady/`: wzorcowe specyfikacje A2 (przykładowa kursantka „Marta”, dane fikcyjne).

Zasady: losowy 10-znakowy slug w `c/`, tylko imię kursanta, `noindex` na każdej stronie.
