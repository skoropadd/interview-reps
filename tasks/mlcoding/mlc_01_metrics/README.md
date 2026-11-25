# mlc_01 · Precision, recall and F1 from scratch

**Task.** Write three functions for binary labels (lists of 0 and 1 of equal length).
- `confusion(y_true, y_pred)` returns the tuple `(tp, fp, fn, tn)`.
- `precision_recall(y_true, y_pred)` returns `(precision, recall)`. When a denominator is zero, that value is `0.0`.
- `f1(y_true, y_pred)` returns the harmonic mean of the two, or `0.0` when both are zero.
- Lists of different lengths raise `ValueError`.

**Then, out loud.** Why a harmonic mean? Which of the two numbers moves when the threshold goes up?

**Conditions.** Blank file, plain Python (no numpy, no sklearn), no autocomplete, 20 minutes. Say the time complexity when you finish.
