import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from debug_01_pipeline import DropMissing, Pipeline, Scale, Step


def test_base_step_run_takes_self():
    assert raises(NotImplementedError, Step("base").run, [])


def test_scale_has_a_name_and_scales():
    step = Scale("price", 2)
    assert step.name == "scale"
    assert step.run([{"price": 10}, {"price": 4}]) == [{"price": 20}, {"price": 8}]


def test_drop_missing_returns_the_kept_rows():
    rows = [{"price": 10}, {"price": None}]
    assert DropMissing("price").run(rows) == [{"price": 10}]


def test_pipelines_do_not_share_steps():
    first = Pipeline()
    first.add(Scale("price", 2))
    assert Pipeline().names() == []


def test_add_can_be_chained_and_run_applies_in_order():
    pipeline = Pipeline().add(DropMissing("price")).add(Scale("price", 3))
    assert pipeline.names() == ["drop_missing", "scale"]
    assert pipeline.run([{"price": 1}, {"price": None}]) == [{"price": 3}]


run(globals())
