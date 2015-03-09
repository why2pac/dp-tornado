# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2015.03.09
#


from ..engine import Engine as dpEngine


class Processor(dpEngine):
    def __init__(self, timeout=None):
        pass

    def run(self):
        raise NotImplementedError