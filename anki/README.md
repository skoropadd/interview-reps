# Anki

**In:** export your deck from Anki (File → Export → "Notes in Plain Text") and save the file here.
Then run `python scripts/reps.py import-anki anki/<file>.txt`. The cards become theory cards in `tasks/theory_anki.json`.

**Out:** during a session, cards for things you got wrong are appended to `anki/new-cards.csv`
as `Front;Back` lines, ready to import into Anki.
