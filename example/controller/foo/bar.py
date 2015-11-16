# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class BarController(Controller):
    # URL matching with /foo/bar, foo/bar/val1, foo/bar/val1/val2
    def get(self, a=None, b=None):
        self.finish('bar controller (%s, %s)' % (a, b))
