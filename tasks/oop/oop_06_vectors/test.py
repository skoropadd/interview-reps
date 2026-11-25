import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from oop_06_vectors import DenseVector, SparseVector, Vector


def test_vector_is_abstract():
    assert raises(TypeError, Vector)
    assert issubclass(DenseVector, Vector) and issubclass(SparseVector, Vector)


def test_dense_takes_one_list():
    v = DenseVector([1, 2, 3])
    assert len(v) == 3
    assert v.dot(DenseVector([4, 5, 6])) == 32


def test_dense_length_mismatch_raises():
    assert raises(ValueError, DenseVector([1, 2]).dot, DenseVector([1, 2, 3]))


def test_sparse_len_is_full_size():
    assert len(SparseVector(1000, {3: 2.0})) == 1000


def test_sparse_dot_only_shared_indexes_count():
    a = SparseVector(10, {0: 1, 3: 2, 7: 5})
    b = SparseVector(10, {3: 4, 8: 9})
    assert a.dot(b) == 8 and b.dot(a) == 8


def test_sparse_dot_with_no_overlap_is_zero():
    assert SparseVector(5, {0: 1}).dot(SparseVector(5, {4: 1})) == 0


def test_sparse_length_mismatch_raises():
    assert raises(ValueError, SparseVector(5, {0: 1}).dot, SparseVector(6, {0: 1}))


def test_sparse_rejects_bad_index():
    assert raises(ValueError, SparseVector, 3, {3: 1.0})
    assert raises(ValueError, SparseVector, 3, {-1: 1.0})


run(globals())
