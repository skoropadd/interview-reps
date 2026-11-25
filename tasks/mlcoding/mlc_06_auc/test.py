import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from mlc_06_auc import roc_auc


def test_perfect_and_reversed():
    assert roc_auc([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9]) == 1.0
    assert roc_auc([1, 1, 0, 0], [0.1, 0.2, 0.8, 0.9]) == 0.0


def test_known_value():
    assert abs(roc_auc([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]) - 0.75) < 1e-12


def test_ties_count_half():
    assert roc_auc([0, 1], [0.5, 0.5]) == 0.5
    assert abs(roc_auc([0, 0, 1], [0.3, 0.7, 0.7]) - 0.75) < 1e-12


def test_one_class_raises():
    assert raises(ValueError, roc_auc, [1, 1], [0.2, 0.9])
    assert raises(ValueError, roc_auc, [0, 0], [0.2, 0.9])


run(globals())
