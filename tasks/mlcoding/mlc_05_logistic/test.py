import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

import math

from mlc_05_logistic import fit, log_loss, predict_proba, sigmoid

X = [[0.5], [1.0], [1.5], [3.0], [3.5], [4.0]]
Y = [0, 0, 0, 1, 1, 1]


def test_sigmoid():
    assert sigmoid(0) == 0.5
    assert abs(sigmoid(2) - 0.8807970779778823) < 1e-12
    assert abs(sigmoid(-2) + sigmoid(2) - 1) < 1e-12


def test_predict_proba():
    assert abs(predict_proba([0.7, -0.2], 0.1, [1, 2]) - sigmoid(0.4)) < 1e-12


def test_log_loss_value_and_clipping():
    assert abs(log_loss([1, 0], [0.9, 0.2]) - (-(math.log(0.9) + math.log(0.8)) / 2)) < 1e-12
    assert log_loss([1], [0.0]) < 30


def test_one_step_from_zero_matches_the_formula():
    weights, bias = fit([[1.0], [3.0]], [0, 1], lr=0.1, epochs=1)
    assert abs(weights[0] - 0.05) < 1e-12 and abs(bias) < 1e-12


def test_fit_separates_the_classes_and_lowers_the_loss():
    weights, bias = fit(X, Y, lr=0.5, epochs=2000)
    probs = [predict_proba(weights, bias, x) for x in X]
    assert [round(p) for p in probs] == Y
    assert log_loss(Y, probs) < log_loss(Y, [0.5] * 6)
    assert weights[0] > 0


run(globals())
