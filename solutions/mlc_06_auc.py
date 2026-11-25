def roc_auc(y_true, scores):
    positives = [s for y, s in zip(y_true, scores) if y == 1]
    negatives = [s for y, s in zip(y_true, scores) if y == 0]
    if not positives or not negatives:
        raise ValueError("need at least one positive and one negative")
    wins = 0.0
    for p in positives:
        for n in negatives:
            if p > n:
                wins += 1
            elif p == n:
                wins += 0.5
    return wins / (len(positives) * len(negatives))

# O(n log n): sort by score, give ranks (average ranks for ties), then
# AUC = (sum of positive ranks - P(P + 1) / 2) / (P * N).
# Under heavy imbalance the many easy negatives keep AUC high; look at PR-AUC.
