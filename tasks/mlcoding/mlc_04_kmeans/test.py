import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from mlc_04_kmeans import kmeans

PTS = [[1, 1], [1, 2], [2, 1], [8, 8], [9, 8], [8, 9]]


def test_two_clear_clusters():
    centroids, labels = kmeans(PTS, [[0, 0], [10, 10]])
    assert labels == [0, 0, 0, 1, 1, 1]
    assert all(abs(a - b) < 1e-9 for a, b in zip(centroids[0], [4 / 3, 4 / 3]))
    assert all(abs(a - b) < 1e-9 for a, b in zip(centroids[1], [25 / 3, 25 / 3]))


def test_bad_start_still_converges():
    _, labels = kmeans(PTS, [[1, 1], [1, 2]], iterations=20)
    assert labels[0] == labels[2] and labels[3] == labels[4] == labels[5] and labels[0] != labels[3]


def test_empty_cluster_keeps_its_centroid():
    centroids, labels = kmeans([[0, 0], [1, 1]], [[0.5, 0.5], [100, 100]])
    assert labels == [0, 0] and centroids[1] == [100, 100]


def test_does_not_change_the_callers_centroids():
    start = [[0, 0], [10, 10]]
    kmeans(PTS, start)
    assert start == [[0, 0], [10, 10]]


def test_one_dimension():
    centroids, labels = kmeans([[1], [2], [10], [11]], [[0], [5]])
    assert labels == [0, 0, 1, 1] and centroids == [[1.5], [10.5]]


run(globals())
