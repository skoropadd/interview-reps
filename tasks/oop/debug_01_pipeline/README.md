# debug_01 · Find the bugs: a feature pipeline

The starter file has **six bugs**. Some crash, some silently give wrong results.

1. Read the code first, without running it, and write down every bug you can find.
2. Then fix them in `work/debug_01_pipeline.py` until the tests pass.
3. For each bug, say in one sentence what was wrong and why it matters.

What the code should do:
- `Step` is a base class with a `name` and a `run(rows)` method.
- `Scale(Step)` multiplies the value under `column` by `factor` in every row.
- `DropMissing(Step)` removes rows where `column` is `None`.
- `Pipeline` holds steps; `add` appends one and returns the pipeline so calls can be chained; `run` applies the steps in order and returns the rows.

This is a common interview format: reading and debugging someone else's classes.
