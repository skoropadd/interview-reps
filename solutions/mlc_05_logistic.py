import math


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


def predict_proba(weights, bias, x):
    return sigmoid(bias + sum(w * value for w, value in zip(weights, x)))


def log_loss(y, p):
    total = 0.0
    for actual, prob in zip(y, p):
        prob = min(max(prob, 1e-12), 1 - 1e-12)
        total += -(actual * math.log(prob) + (1 - actual) * math.log(1 - prob))
    return total / len(y)


def fit(X, y, lr=0.1, epochs=1000):
    n, d = len(X), len(X[0])
    weights, bias = [0.0] * d, 0.0
    for _ in range(epochs):
        errors = [predict_proba(weights, bias, x) - actual for x, actual in zip(X, y)]   # p - y per row
        for j in range(d):
            weights[j] -= lr * sum(e * x[j] for e, x in zip(errors, X)) / n
        bias -= lr * sum(errors) / n
    return weights, bias

# The derivative of log loss through the sigmoid simplifies to (p - y) x.
# A weight of 0.7: one unit more of x multiplies the odds by e^0.7, about 2.
