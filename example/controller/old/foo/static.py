# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class StaticController(Controller):
    def get(self):
        self.render('foo/bar/index.html')
