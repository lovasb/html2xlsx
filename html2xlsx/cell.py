from dateutil.parser import parse
from xlsxwriter.format import Format

class Cell(object):
    def __init__(self, content, content_data_type=None):
        self._content = unicode(content)
        self._type = content_data_type

    @property
    def value(self):
        if self._type == 'number':
            try:
                return int(self._content)
            except ValueError:
                return float(self._content)
        elif self._type == 'date':
            return parse(self._content)
        return unicode(self._content)

    @property
    def format(self):
        if self._type == 'date':
            return {'num_format': 'YYYY-mm-dd'}
        return {}