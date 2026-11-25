from collections import Counter


def knn_predict(train_X, train_y, x, k):
    if k < 1 or k > len(train_X):
        raise ValueError("k must be between 1 and the number of training points")
    distances = []
    for point, label in zip(train_X, train_y):
        squared = sum((a - b) ** 2 for a, b in zip(point, x))   # no sqrt needed: the order is the same
        distances.append((squared, label))
    distances.sort(key=lambda pair: pair[0])
    votes = Counter(label for _, label in distances[:k])
    top = max(votes.values())
    return min(label for label, count in votes.items() if count == top)

# Supervised. Training costs nothing (it stores the data); one prediction is O(n d) for the distances
# plus O(n log n) for the sort. Unscaled features with large units dominate the distance.
