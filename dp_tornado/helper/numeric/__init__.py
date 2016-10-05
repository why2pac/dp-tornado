# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import re


class NumericHelper(dpHelper):
    def extract_numbers(self, string):
        if self.helper.system.py_version <= 2:
            types = basestring,
            types_num = (int, long)
        else:
            types = str,
            types_num = (int, )

        if isinstance(string, types_num):
            return str(string)

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

    def int(self, a, raise_exception=True):
        try:
            if self.helper.system.py_version <= 2:
                return int(a) if a else 0
            else:
                return int(a) if a else 0

        except ValueError as e:
            if raise_exception:
                raise e

            return False

    def long(self, a, raise_exception=True):
        try:
            if self.helper.system.py_version <= 2:
                return long(a) if a else long(0)
            else:
                return int(a) if a else 0

        except ValueError as e:
            if raise_exception:
                raise e

            return False

    @property
    def xxx(self):
        return 'ABtQR5JxfghijN_qrb4KSy9-Uuvw6ZVcLnpMFGkeTPd3WXYEHCDma78sz12'

    def to_xxx(self, x):
        __ = self.xxx
        _ = ''

        while (True):
            if x <= 0:
                break

            k = x % len(__)
            _ = '%s%s' % (__[k:k+1], _)
            x = self.long(x / len(__))

        return _

    def from_xxx(self, x):
        __ = self.xxx
        _ = 0
        c = 0

        for i in reversed(str(x)):
            i = __.find(i)
            _ += i * (len(__) ** c)
            c += 1

        return _
