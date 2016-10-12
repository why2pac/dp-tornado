# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class TrimController(Controller):
    def get(self):
        assert(self.render_string('tests/view/ui_methods/trim.html', {'val': 'abcd'}) == 'abcd')
        assert(self.render_string('tests/view/ui_methods/trim.html', {'val': 'abcd  '}) == 'abcd')
        assert(self.render_string('tests/view/ui_methods/trim.html', {'val': '  abcd'}) == 'abcd')
        assert(self.render_string('tests/view/ui_methods/trim.html', {'val': 'ab  cd'}) == 'ab  cd')
