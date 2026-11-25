from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def fit(self, X, y):
        ...

    @abstractmethod
    def predict(self, X):
        ...

    def score(self, X, y):
        predictions = self.predict(X)
        return sum(abs(p - t) for p, t in zip(predictions, y)) / len(y)


class MeanModel(Model):
    def fit(self, X, y):
        self.mean_ = sum(y) / len(y)
        return self

    def predict(self, X):
        return [self.mean_ for _ in X]
