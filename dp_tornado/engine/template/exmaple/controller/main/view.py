# -*- coding: utf-8 -*-

from dp_tornado.engine.controller import Controller as dpController


class ViewController(dpController):
    def get(self):
        self.render('main/index.html')
