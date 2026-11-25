def add_feature(name, value, features={}):
    features[name] = value
    return features


def scale(rows, key):
    top = max(row[key] for row in rows)
    for row in rows:
        row[key] = row[key] / top
    return rows


first = add_feature("amount", 120)
second = add_feature("country", "NL")
print(first)
print(first is second)

raw = [{"amount": 50}, {"amount": 200}]
scaled = scale(raw, "amount")
print(raw[0]["amount"], scaled is raw)

names = ["amount", "age", "country"]
kinds = ["num", "num", "cat"]
numeric = [n for n, k in zip(names, kinds) if k == "num"]
lookup = {n: i for i, n in enumerate(names, start=1)}
print(numeric, lookup["country"])
