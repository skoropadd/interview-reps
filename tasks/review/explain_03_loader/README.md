# explain_03 · Read and explain: a loader with try, except and finally

Read the code. Do not run it. Answer in the chat, in your own words, one sentence per question first.

```python
class LoadError(Exception):
    pass


def parse(line):
    user, amount = line.split(",")
    return user.strip(), float(amount)


def load(lines):
    rows, bad = [], 0
    for number, line in enumerate(lines, start=1):
        try:
            rows.append(parse(line))
        except ValueError:
            bad += 1
            print(f"line {number} skipped")
        finally:
            last = number
    if not rows:
        raise LoadError("nothing loaded")
    return rows, bad, last


data = ["ann, 10.5", "bob", "cy, x", "dee,3"]
rows, bad, last = load(data)
print(rows)
print(bad, last)
print(sorted(rows, key=lambda r: r[1], reverse=True)[0])
totals = {}
for user, amount in rows:
    totals[user] = totals.get(user, 0) + amount
print(totals)
try:
    load(["oops"])
except LoadError as err:
    print("failed:", err)
```

**Questions**

1. What is printed, line by line?
2. Lines "bob" and "cy, x" both raise `ValueError`, but from different places. Where exactly?
3. What does `finally` do here, and what is `last` after the loop?
4. Why is `LoadError` its own class, and what would the last `try` block do if it caught `ValueError` instead?

**Conditions.** 10 minutes. An interviewer wants to hear the output first, then the reason.
