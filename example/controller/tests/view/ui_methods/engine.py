# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class EngineController(Controller):
    def get(self):
        expect = ','.join(['2016>01>02', '2016&gt;01&gt;02'])
        render = ','.join(self.render_string('tests/view/ui_methods/engine.html').split('\n'))

        assert(expect == render)
