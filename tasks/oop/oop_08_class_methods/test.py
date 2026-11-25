import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from oop_08_class_methods import BusinessCustomer, Customer


def test_method_kinds():
    assert isinstance(Customer.__dict__["valid_id"], staticmethod)
    assert isinstance(Customer.__dict__["from_row"], classmethod)
    assert isinstance(Customer.__dict__["add_high_risk"], classmethod)


def test_valid_id_without_an_object():
    assert Customer.valid_id("C00042")
    assert not Customer.valid_id("C42") and not Customer.valid_id("X00042") and not Customer.valid_id("C0004a")


def test_init_rejects_a_bad_id():
    assert raises(ValueError, Customer, "42", "NL")


def test_count_is_shared_and_counts_subclasses():
    before = Customer.count
    a = Customer("C00001", "NL")
    b = BusinessCustomer("C00002", "DE")
    assert Customer.count == before + 2
    assert "count" not in vars(a) and "count" not in vars(b), "count must stay on the class"
    assert "count" not in vars(BusinessCustomer), "one shared counter, on Customer"


def test_from_row():
    c = Customer.from_row(" C00042 , NL ")
    assert isinstance(c, Customer) and c.customer_id == "C00042" and c.country == "NL"


def test_from_row_on_the_subclass_builds_the_subclass():
    b = BusinessCustomer.from_row("C00077,DE")
    assert type(b) is BusinessCustomer
    assert "from_row" not in vars(BusinessCustomer)


def test_high_risk_is_shared():
    c = Customer("C00003", "ZZ")
    b = BusinessCustomer("C00004", "ZZ")
    assert not c.is_high_risk()
    Customer.add_high_risk("ZZ")
    assert c.is_high_risk() and b.is_high_risk()
    assert "high_risk" not in vars(c)


run(globals())
