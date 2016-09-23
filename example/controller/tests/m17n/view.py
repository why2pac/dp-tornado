# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class ViewController(Controller):
    def get(self, lang=None):
        # If `lang` does not specified, m17n lang will be loaded default or previous switched.

        params = {
            'lang': lang
        }

        self.render('tests/m17n/hello.html', params)
