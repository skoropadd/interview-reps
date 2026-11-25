# oop_03 · Inheritance and super(): SavingsAccount

**Theory in three lines**
- `class SavingsAccount(BankAccount)` gets every method of `BankAccount` for free and can add or replace some.
- If the subclass has its own `__init__`, it must call `super().__init__(...)` so the parent sets up its attributes. Forgetting this is the classic bug.
- Overriding means defining a method with the same name. Inside it, `super().withdraw(amount)` still runs the parent's version.

**Task.** The starter file already contains `BankAccount`. Add `SavingsAccount(BankAccount)`:
- `SavingsAccount(owner, balance=0, rate=0.02, min_balance=0)`. Use `super().__init__` for owner and balance.
- `add_interest()` adds `balance * rate` to the balance and returns the new balance.
- `withdraw(amount)` raises `ValueError` if the balance would fall below `min_balance`. Otherwise it behaves like the parent's `withdraw`, by calling it.
- `deposit` must work unchanged, without you writing it again.
