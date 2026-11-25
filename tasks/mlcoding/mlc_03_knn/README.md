# mlc_03 · k nearest neighbours from scratch

**Task.** Write `knn_predict(train_X, train_y, x, k)`.
- `train_X` is a list of points (lists of numbers), `train_y` their labels, `x` one new point.
- Use Euclidean distance. Take the `k` closest training points and return the most common label among them.
- If two labels tie, return the smaller label.
- `k` larger than the number of training points, or `k < 1`, raises `ValueError`.

**Then, out loud.** Is this supervised or unsupervised? What does "training" cost, and what does one prediction cost? Why scale the features first?

**Conditions.** Blank file, plain Python (no numpy, no sklearn), no autocomplete, 20 minutes. Say the time complexity when you finish.
