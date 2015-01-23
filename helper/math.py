# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.11.04
#


from __future__ import absolute_import
from engine.helper import Helper as dpHelper

import math


class MathHelper(dpHelper):
    def floor(self, x):
        return math.floor(x)

    def ceil(self, x):
        return math.ceil(x)

    def round(self, number, ndigits=None):
        return round(number, ndigits)