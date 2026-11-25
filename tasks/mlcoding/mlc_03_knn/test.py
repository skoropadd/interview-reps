import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from mlc_03_knn import knn_predict

X = [[0, 0], [0, 1], [1, 0], [5, 5], [5, 6], [6, 5]]
Y = ["legit", "legit", "legit", "fraud", "fraud", "fraud"]


def test_nearest_cluster_wins():
    assert knn_predict(X, Y, [0.2, 0.3], 3) == "legit"
    assert knn_predict(X, Y, [5.5, 5.5], 3) == "fraud"


def test_k_equal_one_returns_the_closest_label():
    assert knn_predict(X, Y, [4, 4], 1) == "fraud"


def test_tie_goes_to_the_smaller_label():
    assert knn_predict([[0], [1], [2], [3]], [1, 0, 1, 0], [1.5], 4) == 0
    assert knn_predict(X, Y, [2.5, 2.5], 6) == "fraud"


def test_bad_k_raises():
    assert raises(ValueError, knn_predict, X, Y, [0, 0], 7)
    assert raises(ValueError, knn_predict, X, Y, [0, 0], 0)


run(globals())
