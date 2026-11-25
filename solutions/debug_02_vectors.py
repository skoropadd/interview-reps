# The five bugs:
# 1. DenseVector.__init__ took *values, so DenseVector([1, 2, 3]) stored a tuple holding one list.
# 2. DenseVector implemented dot_product, not dot, so the abstract method was missing (TypeError on creation).
# 3. The length check returned the ValueError instead of raising it.
# 4. SparseVector.__len__ returned the number of non-zero entries, not the full size.
# 5. SparseVector.dot used large[index], a KeyError for indices missing in the other vector; use .get(index, 0).
# Complexity: dense is O(n); sparse is O(min(k1, k2)) for k non-zero entries, worth it when most entries are zero.
from abc import ABC, abstractmethod


class Vector(ABC):
    @abstractmethod
    def dot(self, other):
        ...

    @abstractmethod
    def __len__(self):
        ...


class DenseVector(Vector):
    def __init__(self, values):
        self.values = values

    def __len__(self):
        return len(self.values)

    def dot(self, other):
        if len(self) != len(other):
            raise ValueError("vectors must have the same length")
        return sum(a * b for a, b in zip(self.values, other.values))


class SparseVector(Vector):
    def __init__(self, size, entries):
        self.size = size
        self.entries = entries

    def __len__(self):
        return self.size

    def dot(self, other):
        if len(self) != len(other):
            raise ValueError("vectors must have the same length")
        small, large = self.entries, other.entries
        if len(small) > len(large):
            small, large = large, small
        return sum(value * large.get(index, 0) for index, value in small.items())
