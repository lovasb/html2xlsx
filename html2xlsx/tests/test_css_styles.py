from unittest import TestCase
from .utils import generate_test_html
from html2xlsx.parser import InputParser
from html2xlsx import Table, Sheet, Row, Cell

class CssStylingTest(TestCase):
    def test_styling1(self):
        html = """
                <html>
                <head>
                    <style>
                        td { width: 3cm; font: 15px Arial, serif; }
                        tr.first td { vertical-align: middle; }
                    </style>
                </head>
                <body>
                    <table class='sheet' data-name='First sheet'>
                        <tr style="height: 30px" class="first">
                            <td style="background-color: #eee; font-weight: bold;">1</td>
                            <td style="font-size: 10px; font-style: italic; color: red;">2</td>
                        </tr>
                        <tr>
                            <td style="text-align: center;">3</td>
                            <td style="border: 2px solid blue;">4</td>
                        </tr>
                        <tr>
                            <td colspan=2>asdf</td>
                        </tr>
                    </table>
                </body>
                </html>"""
        html = generate_test_html(html)
        parser = InputParser(html)
        table = parser.parse()
        table.to_workbook('/tmp/proba.xlsx')
