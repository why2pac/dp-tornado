# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import uuid
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

    def uuid(self):  # make a UUID based on the host ID and current time
        return str(uuid.uuid1())
