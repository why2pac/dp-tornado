# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class Nl2brController(Controller):
    def get(self):
        n2b_p = {'args': ['<Hello>,\nWorld.'], 'kwargs': {}}
        n2b_p_ne = {'args': ['<Hello>,\nWorld.'], 'kwargs': {'escape': False}}
        n2b_p_hr = {'args': ['<Hello>,\nWorld.'], 'kwargs': {'escape': False, 'break_tag': '<hr>'}}

        assert(self.render_string('tests/view/ui_methods/nl2br.html', n2b_p) == '&lt;Hello&gt;,<br />World.')
        assert(self.render_string('tests/view/ui_methods/nl2br.html', n2b_p_ne) == '<Hello>,<br />World.')
        assert(self.render_string('tests/view/ui_methods/nl2br.html', n2b_p_hr) == '<Hello>,<hr>World.')
