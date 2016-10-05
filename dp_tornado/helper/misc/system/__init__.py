# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import sys


class SystemHelper(dpHelper):
    @property
    def py_version(self):
        return sys.version_info[0]
