# debug_02 · Find the bugs: dense and sparse vectors

The starter file has **five bugs**.

1. Read first and list the bugs.
2. Fix them in `work/debug_02_vectors.py` until the tests pass.
3. Then answer out loud: what is the time complexity of each `dot`, and when is the sparse version worth it?

What the code should do:
- `Vector` is an abstract base class with abstract methods `dot(other)` and `__len__`.
- `DenseVector(values)` takes one list. `dot` multiplies element by element and sums; vectors of different lengths raise `ValueError`.
- `SparseVector(size, entries)` takes the full length and a dict of `{index: value}` for the non-zero entries. `dot` with another `SparseVector` loops over the smaller dict and looks up the other.

A classic live-coding task turned into a debugging exercise.
