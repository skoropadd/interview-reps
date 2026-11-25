import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from oop_01_bank_account import BankAccount


def test_starts_with_given_balance():
    assert BankAccount("Ana").balance == 0
    assert BankAccount("Ana", 50).balance == 50
    assert BankAccount("Ana", 50).owner == "Ana"


def test_deposit_returns_new_balance():
    acc = BankAccount("Ana", 50)
    assert acc.deposit(25) == 75
    assert acc.balance == 75


def test_withdraw_returns_new_balance():
    acc = BankAccount("Ana", 50)
    assert acc.withdraw(20) == 30


def test_bad_amounts_raise_value_error():
    acc = BankAccount("Ana", 50)
    assert raises(ValueError, acc.deposit, 0)
    assert raises(ValueError, acc.deposit, -5)
    assert raises(ValueError, acc.withdraw, 0)
    assert raises(ValueError, acc.withdraw, 51)
    assert acc.balance == 50


def test_repr():
    assert repr(BankAccount("Ana", 50)) == "BankAccount(owner='Ana', balance=50)"


def test_accounts_do_not_share_state():
    a, b = BankAccount("Ana"), BankAccount("Ben")
    a.deposit(10)
    assert b.balance == 0


run(globals())
