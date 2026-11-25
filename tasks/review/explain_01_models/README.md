# explain_01 · Read and explain: a small class hierarchy

Read the code. Do not run it. Answer in the chat, in your own words, one sentence per question first.

```python
class Model:
    registry = []

    def __init__(self, name):
        self.name = name
        Model.registry.append(name)

    def describe(self):
        return f"{self.kind()} model {self.name}"

    def kind(self):
        return "generic"


class TreeModel(Model):
    def __init__(self, name, depth=3):
        super().__init__(name)
        self.depth = depth

    def kind(self):
        return f"tree(depth={self.depth})"


class Stump(TreeModel):
    def __init__(self, name):
        self.depth = 99
        super().__init__(name, depth=1)


a = Model("base")
b = TreeModel("gbm")
c = Stump("tiny")
print(a.describe())
print(b.describe())
print(c.describe())
print(Model.registry, c.registry is a.registry)
print(isinstance(c, TreeModel), isinstance(b, Stump))
```

**Questions**

1. What do the five `print` lines show? Write the output before anything else.
2. Walk through `Stump("tiny")` line by line. Which `__init__` runs when, and what is `self.depth` at each step?
3. `describe` is defined once, on `Model`. Why does it give a different text for `b` and `c`?
4. `registry` is written as `Model.registry.append(name)`. What kind of attribute is it, and what would change with `self.registry = [name]`?

**Conditions.** 10 minutes. An interviewer wants to hear the output first, then the reason.
