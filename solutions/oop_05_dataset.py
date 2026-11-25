class Dataset:
    def __init__(self, rows):
        self.rows = list(rows)          # a copy: the caller's list stays the caller's

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, key):
        if isinstance(key, slice):      # ds[1:3] arrives here as a slice object
            return Dataset(self.rows[key])
        return self.rows[key]

    def __iter__(self):
        return iter(self.rows)

    def __contains__(self, row):
        return row in self.rows

    def filter(self, keep):
        return Dataset([row for row in self.rows if keep(row)])

    def column(self, name):
        return [row[name] for row in self.rows]   # row[name] raises KeyError by itself

    def __repr__(self):
        count = len(self.rows)
        return f"Dataset({count} row{'' if count == 1 else 's'})"
