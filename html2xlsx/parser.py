import six
from io import BytesIO
from StringIO import StringIO
from lxml import etree


class HTMLTableParser(object):
    def __init__(self, raw):
        self._input = raw
        if isinstance(raw, six.string_types):
            self._root = etree.fromstring(raw)
        elif isinstance(raw, (BytesIO, StringIO)):
            self._root = etree.parse(raw)
        else:
            raise NotImplementedError

    def generate_table(self, html):
        print self._root



if __name__ == '__main__':
    html = "<table><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>"
    pars = HTMLTableParser(html)
    pars.generate_table(html)