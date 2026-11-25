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
