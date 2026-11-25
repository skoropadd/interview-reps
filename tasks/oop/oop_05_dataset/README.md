# oop_05 · A container class: Dataset

**Theory in four lines**
- `len(obj)` calls `obj.__len__()`. `obj[i]` calls `obj.__getitem__(i)`. `for x in obj` calls `obj.__iter__()`. `x in obj` calls `obj.__contains__(x)`.
- These "dunder" methods are how your own class behaves like a list.
- `obj[1:3]` also calls `__getitem__`, with a `slice` object instead of an int. Check with `isinstance(key, slice)`.
- A method that returns a new object of the same class should build it with `type(self)(...)` or the class name.

**Task.** Write `Dataset`, a small wrapper around a list of rows (each row is a dict).
- `Dataset(rows)` stores a **copy** of the list, so later changes to the caller's list don't leak in.
- `len(ds)` is the number of rows.
- `ds[i]` returns row `i` (negative indexes work). `ds[a:b]` returns a new `Dataset`, not a list.
- `for row in ds` goes through the rows in order.
- `row in ds` is `True` when an equal row is stored.
- `ds.filter(keep)` returns a new `Dataset` with the rows for which `keep(row)` is true. The original is unchanged.
- `ds.column(name)` returns the list of values for that key, and raises `KeyError` if any row lacks it.
- `repr(ds)` is `Dataset(3 rows)` (and `Dataset(1 row)` for one).

**Conditions.** Blank file, no autocomplete, 15 minutes.
