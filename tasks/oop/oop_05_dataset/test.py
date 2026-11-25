import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from oop_05_dataset import Dataset

ROWS = [{"id": 1, "amount": 50, "fraud": 0}, {"id": 2, "amount": 900, "fraud": 1}, {"id": 3, "amount": 20, "fraud": 0}]


def test_len_and_index():
    ds = Dataset(ROWS)
    assert len(ds) == 3
    assert ds[0]["id"] == 1 and ds[-1]["id"] == 3


def test_stores_a_copy_of_the_list():
    rows = list(ROWS)
    ds = Dataset(rows)
    rows.append({"id": 4, "amount": 1, "fraud": 0})
    assert len(ds) == 3


def test_slice_returns_a_dataset():
    part = Dataset(ROWS)[1:]
    assert isinstance(part, Dataset)
    assert len(part) == 2 and part[0]["id"] == 2


def test_iteration_and_membership():
    ds = Dataset(ROWS)
    assert [row["id"] for row in ds] == [1, 2, 3]
    assert {"id": 2, "amount": 900, "fraud": 1} in ds
    assert {"id": 9} not in ds


def test_filter_returns_new_dataset_and_keeps_original():
    ds = Dataset(ROWS)
    fraud = ds.filter(lambda row: row["fraud"] == 1)
    assert isinstance(fraud, Dataset)
    assert len(fraud) == 1 and len(ds) == 3


def test_column():
    ds = Dataset(ROWS)
    assert ds.column("amount") == [50, 900, 20]
    assert raises(KeyError, ds.column, "country")


def test_repr():
    assert repr(Dataset(ROWS)) == "Dataset(3 rows)"
    assert repr(Dataset(ROWS[:1])) == "Dataset(1 row)"


run(globals())
