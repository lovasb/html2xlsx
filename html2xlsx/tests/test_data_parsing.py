import os
import sys

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)

from unittest import TestCase
from html2xlsx.parser import InputParser
from html2xlsx import Table, Sheet, Row, Cell

class DataParsingTest(TestCase):
    def test_parsing1(self):
        html = """
                <table class='sheet' data-name='First sheet'>
                    <tr>
                        <td>1</td>
                        <td>2</td>
                    </tr>
                    <tr>
                        <td>3</td>
                        <td>4</td>
                    </tr>
                </table>"""
        parser = InputParser(html)
        table = parser.parse()
        self.assertIsInstance(table, Table)
        self.assertEqual(len(table.sheets), 1)
        sheet = table.sheets[0]
        self.assertIsInstance(sheet, Sheet)
        self.assertEqual(len(sheet.rows), 2)
        i = 1
        for row in sheet: ## sheet.rows
            self.assertIsInstance(row, Row)
            self.assertEqual(len(row.cells), 2)
            for cell in row: ## row.cells
                self.assertIsInstance(cell, Cell)
                self.assertIsInstance(cell.value, unicode)
                self.assertEqual(cell.value, unicode(i))
                i += 1

    def test_output(self):
        ### TODO: data-type default in header?
        html = """
                <table class='sheet' data-name='First sheet'>
                    <tr>
                        <td>1</td>
                        <td data-type='number'>2</td>
                    </tr>
                    <tr>
                        <td data-type='number'>3</td>
                        <td data-type='date'>2013-12-31</td>
                    </tr>
                </table>"""
        parser = InputParser(html)
        table = parser.parse()
        table.to_workbook('/tmp/proba.xlsx')