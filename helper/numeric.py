# -*- coding: utf-8 -*-
#
#   dp for Tornado
#      YoungYong Park (youngyongpark@gmail.com)
#      2014.11.04
#


from __future__ import absolute_import
from engine.helper import Helper as dpHelper

import re
import sys

py_version = sys.version_info[0]


class NumericHelper(dpHelper):
    def extract_numbers(self, string):
        if py_version == 2:
            types = basestring,
        else:
            types = str,

        if not isinstance(string, types):
            return None

        return re.sub(r'\D+', '', string)

    def number_format(self, value, tsep=',', dsep='.'):
        value = self.extract_numbers(value)

        if not value:
            return '0'

        s = str(value)
        cnt = 0
        numchars = dsep + '0123456789'
        ls = len(s)
        while cnt < ls and s[cnt] not in numchars:
            cnt += 1

        lhs = s[:cnt]
        s = s[cnt:]
        if not dsep:
            cnt = -1
        else:
            cnt = s.rfind(dsep)
        if cnt > 0:
            rhs = dsep + s[cnt+1:]
            s = s[:cnt]
        else:
            rhs = ''

        splt = ''
        while s != '':
            splt = s[-3:] + tsep + splt
            s = s[:-3]

        return lhs + splt[:-1] + rhs