# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.12.12
#


from __future__ import absolute_import
from engine.helper import Helper as dpHelper

import sys


class SystemHelper(dpHelper):
    @property
    def py_version(self):
        return sys.version_info[0]