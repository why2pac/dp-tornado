# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller as dpController


class StarterController(dpController):
    def get(self):
        params = {
        }

        self.render('index.html', params)
