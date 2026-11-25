# oop_08 · Class attributes, class methods and static methods

**Theory in four lines**
- A class attribute lives on the class and is shared. `self.count += 1` reads the shared value but **writes an instance attribute**, so the shared one never moves. Write `Customer.count += 1` or use `cls`.
- `@classmethod` receives the class as `cls`. Typical use: a second constructor, `Customer.from_row(...)`. Return `cls(...)`, not `Customer(...)`, so subclasses get their own type.
- `@staticmethod` receives neither `self` nor `cls`: a plain helper that belongs with the class.
- Ask what the method needs: this object → instance method; the class → class method; neither → static method.

**Task.** Write `Customer` and `BusinessCustomer(Customer)`.
- `Customer(customer_id, country)`. Class attribute `count` goes up by one for every customer created, **including** business customers.
- Class attribute `high_risk = {"XX", "YY"}` (a set of country codes).
- Static method `valid_id(text)`: `True` when the text is "C" followed by exactly five digits.
- `__init__` raises `ValueError` when the id is not valid.
- Class method `from_row(row)`: builds a customer from a string like `"C00042, NL"` (spaces around the parts are allowed).
- Instance method `is_high_risk()`: whether the customer's country is in `high_risk`.
- Class method `add_high_risk(code)`: adds a country for **all** customers.
- `BusinessCustomer.from_row(...)` must return a `BusinessCustomer` without you writing `from_row` again.

**Conditions.** Blank file, no autocomplete, 20 minutes.
