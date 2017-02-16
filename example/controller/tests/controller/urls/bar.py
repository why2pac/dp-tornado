# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller as dpController


class BarController(dpController):
    @dpController.route('^test/bar/(.*)/([0-9]+)/$')  # test/bar/a/1/ -> a/1/c
    def get(self, a, b, c='c'):
        self.finish('%s/%s/%s' % (a, b, c))
