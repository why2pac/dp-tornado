# -*- coding: utf-8 -*-
#
#   dp for Tornado
#      YoungYong Park (youngyongpark@gmail.com)
#      2014.10.23
#


from __future__ import absolute_import
from engine.helper import Helper as dpHelper

import random


class RandomHelper(dpHelper):
    def randint(self, a, b):
        return random.randint(a, b)

    def choice(self, seq):
        return random.choice(seq)

    def numeric(self, length=6):
        return random.randint(10 ** (length - 1), (10 ** length) - 1)

    def sample(self, population, k):
        return random.sample(population, k)