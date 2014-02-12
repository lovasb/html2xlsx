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
            head = table.xpath(".//thead/tr/th")
            if len(head):
                row = sheet.add_row(data=[], is_header=True)
                for th in head:
                    c = Cell(content=th.text)
                    row.add_cell(cell=c)
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


"""
from weasyprint import HTML
from weasyprint.css import get_all_computed_styles

document = HTML(string='''
    <style>
    html { font-size: 10px; line-height: 140% }
    section { font-size: 10px; line-height: 1.4 }
    div, p { font-size: 20px; vertical-align: 50% }
    </style>
    <body><div><section><p></p></section></div></body>
    ''')

style_for = get_all_computed_styles(document)
div = document.root_element.xpath('.//div')
style = style_for(d)
style.font_size

sudo apt-get install libffi-dev
"""