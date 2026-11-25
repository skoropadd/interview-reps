class Step:
    def __init__(self, name):
        self.name = name

    def run(rows):
        raise NotImplementedError


class Scale(Step):
    def __init__(self, column, factor):
        self.column = column
        self.factor = factor

    def run(self, rows):
        for row in rows:
            row[self.column] = row[self.column] * factor
        return rows


class DropMissing(Step):
    def __init__(self, column):
        super().__init__("drop_missing")
        self.column = column

    def run(self, rows):
        kept = [row for row in rows if row[self.column] is not None]


class Pipeline:
    def __init__(self, steps=[]):
        self.steps = steps

    def add(self, step):
        self.steps.append(step)

    def run(self, rows):
        for step in self.steps:
            rows = step.run(rows)
        return rows

    def names(self):
        return [step.name for step in self.steps]
