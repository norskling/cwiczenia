# Narzędzia do generowania materiałów

Skrypty, z których Claude korzysta przy tworzeniu ćwiczeń dla kursantów indywidualnych.

- `generuj_cwiczenia.py spec.json c/<slug>.html`: interaktywne ćwiczenia (wybór, uzupełnianie, przekształcanie, dopasowanie, tekst).
- `generuj_drill.py spec.json c/<slug>.html`: muntlig drill z kartami i odsłanianymi odpowiedziami.
- `styl.css`, `skrypt.js`: wspólny styl Norskling i logika sprawdzania.
- `przyklady/`: wzorcowe specyfikacje A2 (przykładowa kursantka „Marta”, dane fikcyjne).

Zasady: losowy 10-znakowy slug w `c/`, tylko imię kursanta, `noindex` na każdej stronie.
