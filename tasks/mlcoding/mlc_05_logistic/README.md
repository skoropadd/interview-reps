# mlc_05 · Logistic regression with gradient descent

**Task.** Write four functions. One feature vector is a list of numbers; `X` is a list of them.
- `sigmoid(z)`: 1 / (1 + e^(-z)).
- `predict_proba(weights, bias, x)`: sigmoid of bias plus the weighted sum.
- `log_loss(y, p)`: the mean of -[y ln p + (1 - y) ln(1 - p)] over the rows. Clip each `p` to the range [1e-12, 1 - 1e-12] first.
- `fit(X, y, lr=0.1, epochs=1000)`: start from zero weights and zero bias. Each epoch: compute `p` for every row, then update with the **batch** gradient: weight j moves by `-lr * mean((p - y) * x_j)`, the bias by `-lr * mean(p - y)`. Return `(weights, bias)`.

**Then, out loud.** Why is the gradient just (p - y) times x? What does a weight of 0.7 mean for the odds?

**Conditions.** Blank file, plain Python (no numpy, no sklearn), no autocomplete, 20 minutes. Say the time complexity when you finish.
