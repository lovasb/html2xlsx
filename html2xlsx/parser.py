import six
from weasyprint import HTML
from io import BytesIO
from StringIO import StringIO
from .table import Table
from .sheet import Sheet
from .row import Row
from .cell import Cell
from weasyprint.css import get_all_computed_styles


class InputParser(object):
    def __init__(self, raw):
        self._input = raw
        if isinstance(raw, six.string_types):
            document = HTML(string=raw)
        elif isinstance(raw, (BytesIO, StringIO)):
            document = HTML(raw)
        else:
            raise NotImplementedError
            return
        self._root = document.root_element
        self._style_for = get_all_computed_styles(document)

    def parse(self):
        sheets = []
        i = 1
        for table in self._root.xpath("//table[@class='sheet']"):
            name = unicode(table.attrib.get('data-name', 'Sheet%d' % i))
            sheet = Sheet(name)
            head = table.xpath(".//thead/tr/th")
            if len(head):
                row = sheet.add_row(data=[], is_header=True, style=self._style_for(head[0]))
                for th in head:
                    c = Cell(content=th.text, style=self._style_for(th), colspan=th.attrib.get('colspan') or 0)
                    row.add_cell(cell=c)
            trs = table.xpath(".//tbody/tr") if len(table.xpath(".//tbody/tr")) else table.xpath(".//tr")
            for tr in trs:
                row = sheet.add_row(data=[], style=self._style_for(tr))
                for td in tr.xpath(".//td"):
                    c = Cell(content=td.text, content_data_type=td.attrib.get('data-type', None), 
                             style=self._style_for(td), colspan=td.attrib.get('colspan') or 0, num_format=td.attrib.get('data-num-format', None))
                    row.add_cell(cell=c)
            sheets.append(sheet)
            i += 1
        table = Table(sheets=sheets)
        return table
