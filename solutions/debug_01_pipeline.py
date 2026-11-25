# The six bugs:
# 1. Step.run was missing `self`.
# 2. Scale.__init__ never called super().__init__, so `name` was missing.
# 3. Scale.run used `factor` instead of `self.factor` (NameError).
# 4. DropMissing.run built `kept` but did not return it (returned None).
# 5. Pipeline.__init__ used a mutable default `steps=[]`, shared by every pipeline.
# 6. Pipeline.add did not return self, so calls could not be chained.
class Step:
    def __init__(self, name):
        self.name = name

    def run(self, rows):
        raise NotImplementedError


class Scale(Step):
    def __init__(self, column, factor):
        super().__init__("scale")
        self.column = column
        self.factor = factor

    def run(self, rows):
        for row in rows:
            row[self.column] = row[self.column] * self.factor
        return rows


class DropMissing(Step):
    def __init__(self, column):
        super().__init__("drop_missing")
        self.column = column

    def run(self, rows):
        return [row for row in rows if row[self.column] is not None]


class Pipeline:
    def __init__(self, steps=None):
        self.steps = list(steps) if steps else []

    def add(self, step):
        self.steps.append(step)
        return self

    def run(self, rows):
        for step in self.steps:
            rows = step.run(rows)
        return rows

    def names(self):
        return [step.name for step in self.steps]
