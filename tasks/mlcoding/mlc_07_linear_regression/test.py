import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from mlc_07_linear_regression import fit_line, r_squared


def test_exact_line():
    slope, intercept = fit_line([1, 2, 3, 4], [3, 5, 7, 9])
    assert abs(slope - 2) < 1e-12 and abs(intercept - 1) < 1e-12
    assert abs(r_squared([1, 2, 3, 4], [3, 5, 7, 9], slope, intercept) - 1) < 1e-12


def test_noisy_data():
    xs, ys = [1, 2, 3, 4, 5], [2, 4, 5, 4, 5]
    slope, intercept = fit_line(xs, ys)
    assert abs(slope - 0.6) < 1e-12 and abs(intercept - 2.2) < 1e-12
    assert abs(r_squared(xs, ys, slope, intercept) - 0.6) < 1e-12


def test_constant_x_raises():
    assert raises(ValueError, fit_line, [2, 2, 2], [1, 2, 3])


def test_constant_y_gives_r_squared_zero():
    slope, intercept = fit_line([1, 2, 3], [4, 4, 4])
    assert slope == 0 and r_squared([1, 2, 3], [4, 4, 4], slope, intercept) == 0.0


run(globals())
