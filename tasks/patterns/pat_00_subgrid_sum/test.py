import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import run

from pat_00_subgrid_sum import find_subgrid

GRID = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]


def test_top_left_window():
    assert find_subgrid(GRID, 14, 2, 2) == (0, 0)


def test_window_in_the_middle():
    assert find_subgrid(GRID, 34, 2, 2) == (1, 1)


def test_window_at_the_bottom_right_edge():
    assert find_subgrid(GRID, 38, 2, 2) == (1, 2)


def test_non_square_window():
    assert find_subgrid(GRID, 21, 1, 3) == (1, 1)
    assert find_subgrid(GRID, 18, 3, 1) == (0, 1)


def test_first_match_in_row_order():
    assert find_subgrid([[1, 1, 1], [1, 1, 1]], 2, 1, 2) == (0, 0)


def test_whole_matrix():
    assert find_subgrid(GRID, 78, 3, 4) == (0, 0)


def test_no_match_returns_none():
    assert find_subgrid(GRID, 1000, 2, 2) is None


def test_window_larger_than_matrix_returns_none():
    assert find_subgrid(GRID, 10, 4, 1) is None
    assert find_subgrid(GRID, 10, 1, 5) is None


run(globals())
