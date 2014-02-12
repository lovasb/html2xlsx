import six
from lxml import html
from io import BytesIO
from StringIO import StringIO
from html2xlsx import Table, Sheet, Row, Cell


class InputParser(object):
    def __init__(self, raw):
        self._input = raw
        if isinstance(raw, six.string_types):
            self._root = html.fromstring(raw)
        elif isinstance(raw, (BytesIO, StringIO)):
            self._root = html.parse(raw)
        else:
            raise NotImplementedError

    def parse(self):
        sheets = []
        i = 1
        for table in self._root.xpath("//table[@class='sheet']"):
            name = unicode(table.attrib.get('data-name', 'Sheet%d' % i))
            sheet = Sheet(name)
            trs = table.xpath(".//tbody/tr") if len(table.xpath(".//tbody/tr")) else table.xpath(".//tr")
            for tr in trs:
                row = sheet.add_row(data=[])
                for td in tr.xpath(".//td"):
                    c = Cell(content=td.text, content_data_type=td.attrib.get('data-type', None))
                    row.add_cell(cell=c)
            sheets.append(sheet)
            i += 1
        table = Table(sheets=sheets)
        return table