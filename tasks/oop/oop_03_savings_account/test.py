import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _runner import raises, run

from oop_03_savings_account import BankAccount, SavingsAccount


def test_is_a_bank_account():
    assert issubclass(SavingsAccount, BankAccount)
    assert "deposit" not in vars(SavingsAccount), "deposit should be inherited, not rewritten"


def test_parent_attributes_are_set():
    acc = SavingsAccount("Ana", 100)
    assert (acc.owner, acc.balance, acc.rate, acc.min_balance) == ("Ana", 100, 0.02, 0)


def test_inherited_deposit_works():
    assert SavingsAccount("Ana", 100).deposit(50) == 150


def test_add_interest():
    acc = SavingsAccount("Ana", 200, rate=0.1)
    assert abs(acc.add_interest() - 220) < 1e-9
    assert abs(acc.balance - 220) < 1e-9


def test_withdraw_respects_min_balance():
    acc = SavingsAccount("Ana", 100, min_balance=40)
    assert acc.withdraw(60) == 40
    assert raises(ValueError, acc.withdraw, 1)
    assert acc.balance == 40


def test_withdraw_keeps_parent_checks():
    acc = SavingsAccount("Ana", 100)
    assert raises(ValueError, acc.withdraw, -5)
    assert raises(ValueError, acc.withdraw, 500)


run(globals())
