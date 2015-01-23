# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.12.17
#


from engine.controller import Controller as dpController


class TestController(dpController):
    # URL matching with /test/case
    def get(self):
        self.finish('test > case controller.')