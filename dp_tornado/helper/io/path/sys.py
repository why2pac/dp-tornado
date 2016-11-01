# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import sys


class SysHelper(dpHelper):
    def insert(self, i, x):
        return sys.path.insert(i, x)

    def append(self, x):
        return sys.path.append(x)
