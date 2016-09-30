# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class M17nController(Controller):
    def get(self, lang=None):
        # If `lang` does not specified, m17n lang will be loaded default or previous switched.

        # Style 1, expect ko_hello or en_hello with get method
        a = self.m17n.get(self.m17n_lang(lang)).tests.hello

        # Style 2, expect ko_hello or en_hello with anonymous method getter
        b = self.m17n.get(self.m17n_lang(lang))._('tests.hello')

        self.finish('%s/%s' % (a, b))
