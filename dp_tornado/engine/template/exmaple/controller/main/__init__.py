# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller as dpController


class MainController(dpController):
    def get(self):
        self.finish('/main')
