import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from mlc_01_metrics import confusion, f1, precision_recall

Y = [1, 1, 1, 0, 0, 0, 0, 1]
P = [1, 0, 1, 1, 0, 0, 0, 0]


def test_confusion_order_is_tp_fp_fn_tn():
    assert confusion(Y, P) == (2, 1, 2, 3)


def test_precision_and_recall():
    precision, recall = precision_recall(Y, P)
    assert abs(precision - 2 / 3) < 1e-9 and abs(recall - 0.5) < 1e-9


def test_f1():
    assert abs(f1(Y, P) - 4 / 7) < 1e-9


def test_no_predicted_positives_gives_zero_not_a_crash():
    assert precision_recall([1, 0], [0, 0]) == (0.0, 0.0)
    assert f1([1, 0], [0, 0]) == 0.0


def test_no_actual_positives():
    assert precision_recall([0, 0], [1, 0]) == (0.0, 0.0)


def test_length_mismatch_raises():
    assert raises(ValueError, confusion, [1, 0], [1])


run(globals())
