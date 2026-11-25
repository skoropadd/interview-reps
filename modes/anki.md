# Mode: Anki import

1. Ask the learner to export from Anki: File → Export → "Notes in Plain Text", saved into `anki/`.
2. Run `python scripts/reps.py import-anki anki/<file>`.
3. Read `tasks/theory_anki.json` and propose a clean-up before changing anything:
   - duplicates and near-duplicates to merge
   - cards that are too long to answer from memory, to split
   - cards outside the tool's scope, to leave in Anki only
4. Apply only what the learner approves. `tasks/theory_anki.json` is personal and is not committed.
