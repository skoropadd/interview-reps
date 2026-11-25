# oop_01 · A basic class: BankAccount

**Theory in three lines**
- A class is a blueprint; an instance is one object made from it. `__init__` runs when the object is created and sets its attributes on `self`.
- `self` is the object the method was called on. `acc.deposit(50)` is really `BankAccount.deposit(acc, 50)`.
- `__repr__` returns the text shown when you print the object or look at it in a list.

**Task.** Write a class `BankAccount`:
- `BankAccount(owner, balance=0)` stores both.
- `deposit(amount)` adds to the balance and returns the new balance. An amount of 0 or less raises `ValueError`.
- `withdraw(amount)` subtracts and returns the new balance. An amount of 0 or less, or more than the balance, raises `ValueError`.
- `repr(account)` gives `BankAccount(owner='Ana', balance=50)`.

Write it in `work/oop_01_bank_account.py`, from a blank file, with autocomplete off.
