# Mode: add tasks

Tasks live in `tasks/*.json`. Files load in name order, and list order is the order new tasks are introduced.

## Fields

- Every task: `id` (unique), `type` (`warmup`, `theory`, `oop`, `debug`, `pattern` or `case`), `title`.
- `warmup`: `prompt`, `expect`.
- `theory` and `case`: `front`, `back`, optional `tags`.
- `oop` and `debug`: `readme`, `starter`, `test`, `solution` (paths from the repo root).
- `pattern`: a `url` to the problem, or `readme` + `test` + `solution` for a local one. Also `pattern` and `level`.

## Local coding tasks

- The folder is `tasks/oop/<id>/` or `tasks/patterns/<id>/` with `README.md`, `starter.py` (optional) and `test.py`.
- `test.py` imports from a module named exactly `<id>` and ends with `run(globals())` from `tasks/_runner.py`.
- The README opens with theory in three lines, then the task.
- Verify before adding: the solution passes the tests and the starter fails them.
- For a `debug` task, state the number of bugs in the README and list them at the top of the solution file.

## Variants

When the bug log shows a repeated mistake, write one new task that needs the same skill in a different setting. Don't reuse the numbers or names of the failed task.

## After adding

Run `python tests/test_reps.py`. It checks that every referenced file exists.
