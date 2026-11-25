---
name: interview-reps
description: >-
  Daily interview practice session: theory cards, OOP exercises and pattern
  problems, with spaced repetition, a streak and code review. Use when the user
  says "daily practice", "today's session", "let's practise", asks for their
  streak or progress, wants to add tasks or import Anki cards, or wants to
  change the practice tool itself.
argument-hint: "[daily | progress | add | anki | triage | develop]"
---

# interview-reps: router

Find the project root: walk up from this file to the directory that contains both `AGENTS.md` and `modes/`. Resolve every path against it.

1. Read `AGENTS.md`.
2. If `profile/HANDOFF.md` exists, read it.
3. Read `modes/_tutor.md`.
4. Pick the mode from the argument or the user's words, and follow its file:

| Input | Mode file |
|---|---|
| empty, `daily`, "daily practice", "today" | `modes/daily.md` |
| `progress`, "streak", "how am I doing" | `modes/progress.md` |
| `add`, "new tasks", "make a variant" | `modes/add.md` |
| `anki`, "import my cards" | `modes/anki.md` |
| `triage`, "fast pass", "I know most of these cards" | `modes/triage.md` |
| `develop`, anything about changing the tool | `modes/develop.md` |

The hard rules in `AGENTS.md` apply in every mode: the script decides what is due, no solutions before an attempt, the learner writes the code, and nothing is recorded without their agreement.
