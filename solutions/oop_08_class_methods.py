class Customer:
    count = 0
    high_risk = {"XX", "YY"}

    def __init__(self, customer_id, country):
        if not self.valid_id(customer_id):
            raise ValueError(f"bad customer id: {customer_id!r}")
        self.customer_id = customer_id
        self.country = country
        Customer.count += 1            # not self.count += 1: that would create an instance attribute

    @staticmethod
    def valid_id(text):
        return len(text) == 6 and text[0] == "C" and text[1:].isdigit()

    @classmethod
    def from_row(cls, row):
        customer_id, country = [part.strip() for part in row.split(",")]
        return cls(customer_id, country)   # cls, so BusinessCustomer.from_row builds a BusinessCustomer

    @classmethod
    def add_high_risk(cls, code):
        Customer.high_risk.add(code)   # mutate the one shared set

    def is_high_risk(self):
        return self.country in self.high_risk


class BusinessCustomer(Customer):
    pass
