import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from mlc_02_kfold import kfold_indices


def test_even_split():
    folds = kfold_indices(6, 3)
    assert [test for _, test in folds] == [[0, 1], [2, 3], [4, 5]]
    assert folds[1][0] == [0, 1, 4, 5]


def test_uneven_split_gives_extra_rows_to_first_folds():
    assert [test for _, test in kfold_indices(5, 2)] == [[0, 1, 2], [3, 4]]
    assert [len(test) for _, test in kfold_indices(10, 3)] == [4, 3, 3]


def test_every_index_tested_exactly_once_and_no_leak():
    folds = kfold_indices(11, 4)
    seen = sorted(i for _, test in folds for i in test)
    assert seen == list(range(11))
    for train, test in folds:
        assert not set(train) & set(test) and len(train) + len(test) == 11


def test_bad_k_raises():
    assert raises(ValueError, kfold_indices, 5, 1)
    assert raises(ValueError, kfold_indices, 3, 4)


run(globals())
