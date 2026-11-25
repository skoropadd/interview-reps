# pat_00 · Find a fixed-size subgrid with a target sum

A matrix question in the style of a technical screen, with tests.

**Task.** Write `find_subgrid(matrix, target, height, width)`.
- `matrix` is a list of lists of numbers. It does not have to be square.
- Return the `(row, col)` of the top-left corner of the first `height` x `width` subgrid whose entries sum to `target`. "First" means scanning row by row, left to right.
- Return `None` if there is none, or if the subgrid does not fit in the matrix.

**Conditions.** 25 minutes, in a plain document or blank file, talking out loud, no running until you have traced a small example by hand.

**Then.** State the time complexity of your version, and describe how a 2D prefix-sum table would make each window O(1).
