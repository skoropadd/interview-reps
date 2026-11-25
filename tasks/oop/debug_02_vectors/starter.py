from abc import ABC, abstractmethod


class Vector(ABC):
    @abstractmethod
    def dot(self, other):
        ...

    @abstractmethod
    def __len__(self):
        ...


class DenseVector(Vector):
    def __init__(self, *values):
        self.values = values

    def __len__(self):
        return len(self.values)

    def dot_product(self, other):
        if len(self) != len(other):
            return ValueError("vectors must have the same length")
        return sum(a * b for a, b in zip(self.values, other.values))


class SparseVector(Vector):
    def __init__(self, size, entries):
        self.size = size
        self.entries = entries

    def __len__(self):
        return len(self.entries)

    def dot(self, other):
        if len(self) != len(other):
            raise ValueError("vectors must have the same length")
        small, large = self.entries, other.entries
        if len(small) > len(large):
            small, large = large, small
        return sum(value * large[index] for index, value in small.items())
