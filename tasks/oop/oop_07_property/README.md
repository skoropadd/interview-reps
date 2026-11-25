# oop_07 · Encapsulation: properties and a setter that validates

**Theory in four lines**
- `_name` means "internal, please don't touch". `__name` is name-mangled to `_ClassName__name`. Neither is truly private.
- `@property` turns a method into something read like an attribute: `acc.balance`, no brackets.
- `@balance.setter` runs on `acc.balance = 5`. Without a setter, assignment raises `AttributeError`: the attribute is read-only.
- Inside the property, read and write the **underscore** name. `return self.balance` inside `balance` calls itself forever.

**Task.** Write `Transaction`.
- `Transaction(amount, currency="EUR")`.
- `amount` is a property backed by `_amount`. Setting it to a negative number, or to something that is not an int or float, raises `ValueError`. This must also hold in `__init__`.
- `currency` is a property that always returns upper case. Setting it to a string that is not exactly three letters raises `ValueError`.
- `is_large` is a **read-only** property: `True` when the amount is 10,000 or more. Assigning to it raises `AttributeError`.
- `repr(t)` is `Transaction(250.0, 'EUR')` (the amount is stored as a float).

**Conditions.** Blank file, no autocomplete, 15 minutes.
