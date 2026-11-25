import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from oop_07_property import Transaction


def test_defaults_and_repr():
    t = Transaction(250)
    assert t.amount == 250.0 and t.currency == "EUR"
    assert repr(t) == "Transaction(250.0, 'EUR')"


def test_amount_is_a_property_backed_by_underscore_name():
    assert isinstance(Transaction.__dict__["amount"], property)
    assert Transaction(5)._amount == 5.0


def test_amount_validation_on_set_and_in_init():
    t = Transaction(10)
    assert raises(ValueError, setattr, t, "amount", -1)
    assert raises(ValueError, setattr, t, "amount", "12")
    assert raises(ValueError, Transaction, -5)
    assert t.amount == 10.0


def test_currency_is_upper_case_and_three_letters():
    t = Transaction(10, "usd")
    assert t.currency == "USD"
    assert raises(ValueError, setattr, t, "currency", "EURO")
    assert raises(ValueError, setattr, t, "currency", "E1R")
    assert raises(ValueError, Transaction, 10, "")


def test_is_large_is_read_only():
    t = Transaction(9999.99)
    assert t.is_large is False
    t.amount = 10000
    assert t.is_large is True
    assert raises(AttributeError, setattr, t, "is_large", False)


run(globals())
