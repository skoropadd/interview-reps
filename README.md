# interview-reps

Daily practice for data-science interviews: code written by hand, theory from memory, and a tutor that reviews instead of solving.

It combines three things in one short session:

1. **Theory cards**, Anki style: Python fundamentals, statistics, ML and deep-learning basics.
2. **OOP foundations**: a short theory note plus an exercise or a find-the-bugs task, with tests.
3. **Pattern problems**: medium LeetCode-style problems in five patterns, solved on LeetCode or NeetCode and reviewed here.

A script decides what is due (spaced like Anki), runs the tests and keeps the streak. Claude runs the session: it presents the tasks, gives hints in steps, reviews your code like an interviewer and answers follow-up questions.

## Status

Version 0, built on 25 Nov 2026. The scheduler, tests and first task batch work. Not yet used for a real week.

## A session

In Claude Code, opened in this folder, say **"daily practice"** (or run `/interview-reps`).

Or drive it by hand:

```bash
python scripts/reps.py today                      # today's session and your streak
python scripts/reps.py start oop_01_bank_account  # creates work/oop_01_bank_account.py
python scripts/reps.py check oop_01_bank_account  # runs the tests
python scripts/reps.py record oop_01_bank_account clean
python scripts/reps.py progress
```

Results are `clean` (right first time), `errors` (got there with bugs or a hint) or `failed`.

## The week

| Day | Main task |
|---|---|
| Mon, Wed, Fri | A pattern problem |
| Tue | An OOP exercise |
| Thu | A find-the-bugs task |
| Fri | Plus one typed case card |
| Weekend | Optional |

Every session also has a warm-up snippet, five theory cards and one redo.

## Layout

| Path | What it is |
|---|---|
| `scripts/reps.py` | The deterministic core: schedule, tests, record, progress |
| `tasks/*.json` | The task bank. Files load in name order; list order is the curriculum order |
| `tasks/oop/`, `tasks/patterns/` | Task notes, starter files and tests |
| `solutions/` | Reference solutions. Not opened before an attempt |
| `modes/` | Instructions Claude follows for each kind of session |
| `.claude/skills/interview-reps/` | The skill that routes to the modes |
| `data/` | Your progress, log and bug log (not committed) |
| `work/` | Your solutions (not committed) |
| `profile/` | Personal context (not committed) |

Python 3.9 or later, standard library only. Tests: `python tests/test_reps.py`.

## Your card library and flags

`tasks/60_cards.json` holds the Python and statistics cards (400), each with a `track`, a `topic` and a `status`:
`active` (in the rotation), `parked` (kept, switched off until you turn its topic on) or `off` (duplicate or not useful).
Nothing is deleted. Cards you want to keep to yourself go in `tasks/*_personal.json`, which is not committed.

```
python scripts/reps.py library               # per topic: weight, in rotation, parked, off
python scripts/reps.py flag topic:trees on   # switch a parked topic on
python scripts/reps.py flag topic:oop 5      # raise a topic's weight: its new cards come first
python scripts/reps.py flag py_153 off       # switch one card off (or on, or default)
```

Default topic weights are in `config/topics.json`. Your own flags are saved in `profile/focus.json`, which is personal and not committed.

## Session size and the fast pass

```
python scripts/reps.py set theory_per_day 10   # cards per session (default 5)
python scripts/reps.py triage                  # list unseen cards; mark with --known / --weak
```

If you already know many cards, say "fast pass" in Claude Code: you sort unseen cards into known and weak in batches of 15.
Known cards come back spread over the following weeks; weak ones come first in your daily sessions.

## Licence

MIT. See `LICENSE`.
