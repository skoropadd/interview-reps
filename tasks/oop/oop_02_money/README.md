# oop_02 · Equality and hashing: Money

**Theory in three lines**
- By default two objects are equal only if they are the same object. `__eq__` lets you say when two different objects count as equal.
- If you define `__eq__`, Python removes the default `__hash__`, so the object can no longer go in a set or be a dict key. Define `__hash__` too, from the same fields.
- Rule: objects that are equal must have the same hash.

**Task.** Write a class `Money`:
- `Money(amount, currency)`.
- Two `Money` objects are equal when amount and currency both match. Comparing with something that is not `Money` gives `False`, not an error.
- It works in a set: `{Money(5, 'EUR'), Money(5, 'EUR')}` has one element.
- `a + b` returns a new `Money` when the currencies match, and raises `ValueError` when they differ.
- `repr` gives `Money(5, 'EUR')`.
