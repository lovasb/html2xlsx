from webcolors import rgb_to_hex
from dateutil.parser import parse
from xlsxwriter.format import Format

class Cell(object):
    def __init__(self, content, colspan=0, content_data_type=None, style=None):
        self._content = unicode(content)
        self._type = content_data_type
        self._style = style
        self._colspan = colspan

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

    @property
    def width(self):
        if self._style['width'] == 'auto':
            return None
        return self._style['width']

    @property
    def colspan(self):
        return int(self._colspan)

    def get_formatting_style(self, book):
        format_dict = self.format
        if self._style:
            c = self._style['background_color']
            if c.alpha == 1.0:
                format_dict['bg_color'] = rgb_to_hex((c.red * 255, c.green * 255, c.blue * 255))
            if self._style['font_weight'] > 400:
                format_dict['bold'] = True
            format_dict['font_size'] = self._style['font_size']
            if self._style['font_style'] == 'italic':
                format_dict['italic'] = True
            c = self._style['color']
            if c.alpha == 1.0:
                format_dict['font_color'] = rgb_to_hex((c.red * 255, c.green * 255, c.blue * 255))
            if len(self._style['font_family']) > 1:
                format_dict['font_family'] = self._style['font_family'][0]
            if self._style['text_align'] != '-weasy-start':
                format_dict['align'] = self._style['text_align']
            for side in ('left', 'top', 'right', 'bottom'):
                width = self._style['border_left_width']
                if width == 0:
                    continue
                format_dict[side] = 1 ##set width
                c = self._style['border_left_color']
                format_dict['%s_color' % side] = rgb_to_hex((c.red * 255, c.green * 255, c.blue * 255))
            format_dict['valign'] = self._style['vertical_align']
            if format_dict['valign'] not in ('top', 'bottom'):
                format_dict['valign'] = 'vcenter'
        return book.add_format(format_dict)
