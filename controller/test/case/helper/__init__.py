# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.12.18
#


from engine.controller import Controller as dpController


class HelperController(dpController):
    # URL matching with /test/case/helper
    def get(self):
        self.finish('test > case > helper controller.')