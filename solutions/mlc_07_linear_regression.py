def fit_line(xs, ys):
    n = len(xs)
    mean_x, mean_y = sum(xs) / n, sum(ys) / n
    spread = sum((x - mean_x) ** 2 for x in xs)
    if spread == 0:
        raise ValueError("all x values are equal: the slope is undefined")
    slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / spread
    return slope, mean_y - slope * mean_x


def r_squared(xs, ys, slope, intercept):
    mean_y = sum(ys) / len(ys)
    total = sum((y - mean_y) ** 2 for y in ys)
    if total == 0:
        return 0.0
    residual = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys))
    return 1 - residual / total

# Matrix form: beta = (X'X)^-1 X'y. It fails when X'X cannot be inverted: perfectly collinear
# features, or more features than rows. The iterative alternative is gradient descent.
