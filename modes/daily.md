# Mode: daily session

Read `modes/_tutor.md` first.

## Flow

1. Run `python scripts/reps.py today --json`.
2. Open with the progress line from the output: streak, days this week, and one bar per pillar. Keep it to a few lines. If `data/bug-log.md` has entries from the last week, show the two most recent as "watch for".
3. Go through the session in this order. One item at a time; wait for the learner after each.
   - **Warm-up** (about 3 minutes). Show the prompt. They type the code. Compare with `expect`.
   - **Theory cards.** One by one, front first.
   - **Main task.**
     - With a `readme`: show it, run `start <id>`, tell them the file path, wait until they say they're done, then run `check <id>` and review.
     - With `"kind": "explain"`: show the README, no `start` and no `check`. They answer in the chat. See the tutor rules.
     - With a `url`: give the link and the pattern name. They solve it there with autocomplete off, then paste the code and say whether it passed. Review.
     - Remind them of the conditions once: 25 minutes, talk out loud, trace a small example by hand before running anything.
   - **Redo.** Same as the main task. Before they start, show the bug-log note for this task if there is one.
   - **Case card** (Fridays). Show the front. They type for 90 seconds. Compare with the back.
4. After each item, propose a result and record it once they agree:
   `python scripts/reps.py record <id> <result> --note "..."`.
5. Close with `python scripts/reps.py progress` and one line on what comes back tomorrow.

## If time is short

The learner can stop after any item. Whatever was recorded counts; the rest stays due. Never record items that weren't done.

## If they want more

Run `today --refresh` only if every item in the session is recorded. Otherwise offer the unfinished items first.
