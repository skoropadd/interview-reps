class Transaction:
    def __init__(self, amount, currency="EUR"):
        self.amount = amount          # goes through the setter, so __init__ validates too
        self.currency = currency

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        # bool is a subclass of int, so exclude it explicitly
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("amount must be a non-negative number")
        self._amount = float(value)

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        if not isinstance(value, str) or len(value) != 3 or not value.isalpha():
            raise ValueError("currency must be three letters")
        self._currency = value.upper()

    @property
    def is_large(self):               # no setter: read-only
        return self._amount >= 10_000

    def __repr__(self):
        return f"Transaction({self._amount!r}, {self._currency!r})"
