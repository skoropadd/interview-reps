# oop_06 · From a blank file: dense and sparse vectors

You have seen this code as a find-the-bugs task. Now write it yourself.

**Task.**
- `Vector`: an abstract base class with abstract methods `dot(self, other)` and `__len__(self)`.
- `DenseVector(values)`: takes **one list** of numbers. `dot` multiplies element by element and sums.
- `SparseVector(size, entries)`: takes the full length and a dict `{index: value}` of the non-zero entries. `dot` with another `SparseVector` loops over the **smaller** dict and looks up the other one.
- In both classes `len(v)` is the full length, and `dot` raises `ValueError` when the lengths differ.
- `SparseVector` raises `ValueError` at creation if an index is negative or not below `size`.
- `Vector()` raises `TypeError`.

**Conditions.** Blank file, no autocomplete, 20 minutes. Write the simplest version, run it, read the error, fix. Don't talk through options you haven't tried.

**Then, out loud.** Time complexity of each `dot`. When is the sparse version worth it? What would `dot` between a dense and a sparse vector look like?
