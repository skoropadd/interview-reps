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

    def dot(self, other):                      # O(n)
        if len(self) != len(other):
            raise ValueError("vectors must have the same length")
        return sum(a * b for a, b in zip(self.values, other.values))


class SparseVector(Vector):
    def __init__(self, size, entries):
        for index in entries:
            if not 0 <= index < size:
                raise ValueError(f"index {index} is outside 0..{size - 1}")
        self.size = size
        self.entries = entries

    def __len__(self):
        return self.size

    def dot(self, other):                      # O(min(k1, k2)) for k non-zero entries
        if len(self) != len(other):
            raise ValueError("vectors must have the same length")
        small, large = self.entries, other.entries
        if len(small) > len(large):
            small, large = large, small
        return sum(value * large.get(index, 0) for index, value in small.items())

# Dense with sparse: loop over the sparse entries only, sum(value * dense.values[index]): O(k).
