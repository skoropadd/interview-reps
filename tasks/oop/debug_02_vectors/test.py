import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from debug_02_vectors import DenseVector, SparseVector, Vector


def test_vector_is_abstract():
    assert raises(TypeError, Vector)


def test_dense_takes_one_list():
    vector = DenseVector([1, 2, 3])
    assert len(vector) == 3
    assert vector.values == [1, 2, 3]


def test_dense_dot():
    assert DenseVector([1, 2, 3]).dot(DenseVector([4, 5, 6])) == 32


def test_dense_length_mismatch_raises():
    assert raises(ValueError, DenseVector([1, 2]).dot, DenseVector([1, 2, 3]))


def test_sparse_len_is_the_full_size():
    assert len(SparseVector(1000, {3: 2.0})) == 1000


def test_sparse_dot_skips_missing_indices():
    a = SparseVector(1000, {3: 2.0, 500: 1.0})
    b = SparseVector(1000, {3: 4.0, 7: 9.0, 999: 1.0})
    assert a.dot(b) == 8.0
    assert b.dot(a) == 8.0


def test_sparse_length_mismatch_raises():
    assert raises(ValueError, SparseVector(10, {1: 1.0}).dot, SparseVector(11, {1: 1.0}))


run(globals())
