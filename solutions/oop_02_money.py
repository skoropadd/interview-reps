class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def __eq__(self, other):
        if not isinstance(other, Money):
            return False
        return (self.amount, self.currency) == (other.amount, other.currency)

    def __hash__(self):
        return hash((self.amount, self.currency))

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("currencies differ")
        return Money(self.amount + other.amount, self.currency)

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"
