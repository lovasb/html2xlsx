from .row import Row


class Sheet(object):
    def __init__(self, name):
        self._name = name
        self._rows = []

    def add_row(self, data=[]):
        row = Row(data=data)
        self._rows.append(row)
        return row

    @property
    def name(self):
        return self._name

    @property
    def rows(self):
        return self._rows

    def __iter__(self):
        for row in self._rows:
            yield row