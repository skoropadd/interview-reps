# mlc_06 · ROC AUC by counting pairs

**Task.** Write `roc_auc(y_true, scores)`.
- AUC is the probability that a randomly chosen positive gets a higher score than a randomly chosen negative.
- Count over every (positive, negative) pair: 1 when the positive scores higher, 0.5 for a tie, 0 otherwise. Divide by the number of pairs.
- If there are no positives or no negatives, raise `ValueError`.

**Then, out loud.** This version is O(positives x negatives). How would you get O(n log n)? Why can AUC look fine when fraud is 0.1% of the data?

**Conditions.** Blank file, plain Python (no numpy, no sklearn), no autocomplete, 20 minutes. Say the time complexity when you finish.
