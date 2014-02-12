import xlsxwriter

class Table(object):
    def __init__(self, sheets):
        self._sheets = sheets

    def to_workbook(self, io):
        wb = xlsxwriter.Workbook(io)
        for sheet in self.sheets:
            ws = wb.add_worksheet(sheet.name)
            for row in sheet:
                x = sheet.rows.index(row)
                for cell in row:
                    y = row.cells.index(cell)
                    formt = wb.add_format(cell.format)
                    ws.write(x, y, cell.value, formt)
        print len(wb.formats)
        wb.close()


    @property
    def sheets(self):
        return self._sheets

    def __iter__(self):
        for s in self._sheets:
            yield s