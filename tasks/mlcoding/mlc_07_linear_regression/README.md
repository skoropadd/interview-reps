# mlc_07 · Simple linear regression, closed form

**Task.** Write two functions for one feature.
- `fit_line(xs, ys)` returns `(slope, intercept)` by least squares: slope = sum of (x - mean x)(y - mean y) divided by sum of (x - mean x) squared; intercept = mean y - slope times mean x.
- If all `xs` are the same, raise `ValueError` (the slope is undefined).
- `r_squared(xs, ys, slope, intercept)` returns 1 minus (sum of squared residuals divided by total sum of squares around the mean of y). If `ys` are all equal, return `0.0`.

**Then, out loud.** What is the matrix form of this for many features, and when does it fail? What is the iterative alternative?

**Conditions.** Blank file, plain Python (no numpy, no sklearn), no autocomplete, 20 minutes. Say the time complexity when you finish.
