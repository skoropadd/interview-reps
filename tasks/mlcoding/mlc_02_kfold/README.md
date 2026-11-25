# mlc_02 · k-fold split indexes

**Task.** Write `kfold_indices(n, k)`.
- It returns a list of `k` pairs `(train, test)`, each a list of row indexes from `0` to `n - 1`.
- Folds are taken in order, without shuffling. When `n` is not divisible by `k`, the **first** `n % k` folds get one extra row.
- Every index is in exactly one test fold. Train is everything else, in increasing order.
- `k < 2` or `k > n` raises `ValueError`.

Example: `kfold_indices(5, 2)` gives test folds `[0, 1, 2]` and `[3, 4]`.

**Then, out loud.** When is a plain k-fold split wrong for your data (two cases)?

**Conditions.** Blank file, plain Python (no numpy, no sklearn), no autocomplete, 20 minutes. Say the time complexity when you finish.
