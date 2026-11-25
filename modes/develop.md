# Mode: developing the tool

The learner builds this tool with you. Here you write the code; in practice sessions you don't.

- Read `profile/HANDOFF.md` for the backlog and the decisions already made.
- Keep the two layers apart (see `AGENTS.md`). Files in `data/` are the source of truth for progress; anything else is derived.
- Standard library only in `scripts/`, unless the learner agrees to a dependency.
- Every change to `scripts/reps.py` gets a test in `tests/test_reps.py`. Run the tests before saying it works.
- Small steps: one feature, working and tested, then the next.
- When a session is real practice, switch back to `modes/daily.md` and its rules.
