class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        return self.balance


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, rate=0.02, min_balance=0):
        super().__init__(owner, balance)
        self.rate = rate
        self.min_balance = min_balance

    def add_interest(self):
        self.balance += self.balance * self.rate
        return self.balance

    def withdraw(self, amount):
        if amount > 0 and self.balance - amount < self.min_balance:
            raise ValueError("balance would fall below the minimum")
        return super().withdraw(amount)
