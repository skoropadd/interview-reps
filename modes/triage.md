# Mode: fast pass over the theory cards

For a learner who already knows many of the cards. The goal is to sort unseen cards into "known" and "weak" quickly,
so the daily session spends its time on the weak ones. Read `modes/_tutor.md` first.

## Flow

1. Run `python scripts/reps.py triage --json --limit 15` (add `--topic <name>` if they want one topic).
2. Show the batch as a numbered list: number, then the front. No backs, no ids, no commentary.
3. Ask for one line back: the numbers they are NOT sure about. Everything else in the batch counts as known.
   The test to give them: "Could you say the answer in one sentence right now?" If they hesitate, it is weak.
4. Record with one command: `python scripts/reps.py triage --known <ids> --weak <ids>`.
5. Show the summary line (left, known, weak) and ask whether to continue. Stop whenever they say so; the pass can be resumed any day.

## Rules

- This is self-report, so it never counts as a rep, never touches the streak, and never marks a card as mastered.
  Known cards go to box 3 and come back spread out, about five a day, starting four days later. A wrong answer then
  sends the card to box 1 like any other.
- Weak cards stay new and come first in the daily sessions.
- Do not teach during the pass. If they ask about a card, mark it weak and move on.
- Do not show the back of a card here, even for "known" ones.
