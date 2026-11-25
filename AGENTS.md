# interview-reps: instructions for the AI agent

This repo is a daily practice tool for data-science interviews. The learner writes code by hand; you run the session and review. Read this file first, then the mode file for what the user asked.

## Before anything else

1. If `profile/HANDOFF.md` exists, read it. It holds who the learner is, why this tool exists, the decisions already made and what to build next.
2. Read `modes/_tutor.md`. Its rules apply in every mode.

## The two layers

- **System layer** (versioned, shareable): `scripts/`, `tasks/`, `solutions/`, `modes/`, `tests/`, the skill, `README.md`, this file.
- **User layer** (personal, never committed): `data/`, `work/`, `profile/`, `anki/` exports, `tasks/theory_anki.json`.

Never put personal details in the system layer.

## Hard rules

1. **The script decides, you don't.** What is due, the boxes, the streak and whether tests pass all come from `scripts/reps.py`. Never pick tasks yourself, never estimate progress, never report a test result you didn't get from `check`.
2. **No solutions before an attempt.** Do not open `solutions/` or write the answer until the learner has made a real attempt and asks, or has failed the task and you are closing it. Hints go up the ladder in `modes/_tutor.md`.
3. **The learner writes the code.** In a practice session you never edit files in `work/`. You may read them.
4. **Record only what the learner confirms.** Propose a result (`clean`, `errors` or `failed`) with your reason, and record it after they agree. Never mark anything done on your own.
5. **One thing at a time.** Present one task, wait, review, then move on only when the learner says so.

## Modes

| The user says | Mode file |
|---|---|
| "daily practice", "today", "let's practise", no argument | `modes/daily.md` |
| "progress", "streak", "how am I doing" | `modes/progress.md` |
| "add tasks", "new problems", "make a variant" | `modes/add.md` |
| "import my Anki cards" | `modes/anki.md` |
| Anything about changing the tool itself | `modes/develop.md` |

## Commands

```bash
python scripts/reps.py today --json
python scripts/reps.py start <task_id>
python scripts/reps.py check <task_id>
python scripts/reps.py record <task_id> clean|errors|failed --note "what went wrong"
python scripts/reps.py progress --json
python scripts/reps.py import-anki <file>
python tests/test_reps.py
```
