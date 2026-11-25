import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from oop_04_abstract_model import MeanModel, Model


def test_model_cannot_be_instantiated():
    assert raises(TypeError, Model)


def test_incomplete_subclass_cannot_be_instantiated():
    class OnlyFit(Model):
        def fit(self, X, y):
            return self

    assert raises(TypeError, OnlyFit)


def test_mean_model_is_a_model():
    assert issubclass(MeanModel, Model)


def test_fit_returns_self_and_predict_gives_the_mean():
    model = MeanModel()
    assert model.fit([[1], [2], [3]], [10, 20, 30]) is model
    assert model.predict([[5], [6]]) == [20, 20]


def test_score_is_mean_absolute_error_and_is_inherited():
    model = MeanModel().fit([[1], [2]], [10, 30])
    assert "score" not in vars(MeanModel), "score should live on Model"
    assert abs(model.score([[1], [2]], [10, 30]) - 10) < 1e-9


run(globals())
