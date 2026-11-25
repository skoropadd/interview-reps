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
