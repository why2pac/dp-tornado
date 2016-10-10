# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import uuid
import random


class RandomHelper(dpHelper):
    @dpHelper.decorators.deprecated
    def randint(self, a, b):
        return random.randint(a, b)

    @dpHelper.decorators.deprecated
    def choice(self, seq):
        return random.choice(seq)

    @dpHelper.decorators.deprecated
    def numeric(self, length=6):
        return random.randint(10 ** (length - 1), (10 ** length) - 1)

    @dpHelper.decorators.deprecated
    def sample(self, population, k):
        return random.sample(population, k)

    @dpHelper.decorators.deprecated
    def uuid(self):  # make a UUID based on the host ID and current time
        return str(uuid.uuid1())
