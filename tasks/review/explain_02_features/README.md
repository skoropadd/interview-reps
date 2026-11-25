# explain_02 · Read and explain: feature helpers with two traps

Read the code. Do not run it. Answer in the chat, in your own words, one sentence per question first.

```python
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
```

**Questions**

1. What do the four `print` lines show?
2. Why does `first` contain the country? Name the trap and fix `add_feature` in two lines.
3. `scale` returns `rows`. Did it make a new list? What happened to `raw`, and when does that hurt in a pipeline?
4. Say in words what the `numeric` and `lookup` lines build.

**Conditions.** 10 minutes. An interviewer wants to hear the output first, then the reason.
