def kfold_indices(n, k):
    if k < 2 or k > n:
        raise ValueError("k must be between 2 and n")
    base, extra = divmod(n, k)
    folds, start = [], 0
    for fold in range(k):
        size = base + (1 if fold < extra else 0)
        test = list(range(start, start + size))
        train = list(range(0, start)) + list(range(start + size, n))
        folds.append((train, test))
        start += size
    return folds

# Plain k-fold is wrong for time-ordered data (use a time split) and when rows of one customer
# land in both train and test (group the folds by customer).
