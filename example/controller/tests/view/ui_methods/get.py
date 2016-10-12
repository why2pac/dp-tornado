# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class GetController(Controller):
    def get(self):
        p1 = self.get_argument('p1', default='empty')
        p2 = self.get_argument('p2', default='None')

        assert(self.render_string('tests/view/ui_methods/get.html', {'key': 'p1', 'default': 'empty'}) == p1)
        assert(self.render_string('tests/view/ui_methods/get.html', {'key': 'p2', 'default': None}) == p2)
