import xlsxwriter

class Table(object):
    def __init__(self, sheets):
        self._sheets = sheets

    def to_workbook(self, io):
        wb = xlsxwriter.Workbook(io)
        for sheet in self.sheets:
            ws = wb.add_worksheet(sheet.name)
            col = 0
            for cell in sheet.rows[0]:
                if cell.width:
                    ws.set_column(col, col, cell.width.value * 0.1)
                col += 1
            for row in sheet:
                x = sheet.rows.index(row)
                if row.height != 'auto':
                    ws.set_row(x, row.height.value)
                for cell in row:
                    y = row.cells.index(cell)
                    formt = cell.get_formatting_style(wb)
                    if cell.colspan > 0:
                        ws.merge_range(x, y, x, y+cell.colspan-1, cell.value, formt)
                    else:
                        ws.write(x, y, cell.value, formt)
        wb.close()


    @property
    def sheets(self):
        return self._sheets

    def __iter__(self):
        for s in self._sheets:
            yield s
