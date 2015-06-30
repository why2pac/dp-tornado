# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2015.06.30
#


from engine.controller import Controller as dpController


class StaticController(dpController):
    def get(self):
        self.render('foo/bar/index.html')
