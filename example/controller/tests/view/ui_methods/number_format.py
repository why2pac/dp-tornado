# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class NumberFormatController(Controller):
    def get(self):
        assert(self.render_string('tests/view/ui_methods/number_format.html', {'val': '123,45'}) == '12,345')
        assert(self.render_string('tests/view/ui_methods/number_format.html', {'val': '123.45'}) == '123.45')
        assert(self.render_string('tests/view/ui_methods/number_format.html', {'val': 123.45}) == '123.45')
        assert(self.render_string('tests/view/ui_methods/number_format.html', {'val': 123456}) == '123,456')
        assert(self.render_string('tests/view/ui_methods/number_format.html', {'val': '123,456.12'}) == '123,456.12')
        assert(self.render_string('tests/view/ui_methods/number_format.html', {'val': '123,45.12'}) == '12,345.12')
        assert(self.render_string('tests/view/ui_methods/number_format.html', {'val': '123,456'}) == '123,456')
        assert(self.render_string('tests/view/ui_methods/number_format.html', {'val': '123/456'}) == '123,456')
        assert(self.render_string('tests/view/ui_methods/number_format.html', {'val': '123456'}) == '123,456')
