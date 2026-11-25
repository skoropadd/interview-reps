import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from oop_02_money import Money


def test_equal_when_fields_match():
    assert Money(5, "EUR") == Money(5, "EUR")
    assert Money(5, "EUR") != Money(6, "EUR")
    assert Money(5, "EUR") != Money(5, "USD")


def test_not_equal_to_other_types():
    assert (Money(5, "EUR") == 5) is False
    assert (Money(5, "EUR") == "5 EUR") is False


def test_usable_in_a_set_and_as_a_key():
    assert len({Money(5, "EUR"), Money(5, "EUR"), Money(7, "EUR")}) == 2
    prices = {Money(5, "EUR"): "coffee"}
    assert prices[Money(5, "EUR")] == "coffee"


def test_add_same_currency_returns_new_object():
    a, b = Money(5, "EUR"), Money(7, "EUR")
    total = a + b
    assert total == Money(12, "EUR")
    assert a == Money(5, "EUR")


def test_add_different_currency_raises():
    assert raises(ValueError, lambda: Money(5, "EUR") + Money(5, "USD"))


def test_repr():
    assert repr(Money(5, "EUR")) == "Money(5, 'EUR')"


run(globals())
