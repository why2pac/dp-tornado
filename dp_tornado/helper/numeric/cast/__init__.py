# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class CastHelper(dpHelper):
    def int(self, a, raise_exception=False):
        try:
            if self.helper.misc.system.py_version <= 2:
                return int(a) if a else 0
            else:
                return int(a) if a else 0

        except ValueError as e:
            if raise_exception:
                raise e

            return False

    def long(self, a, raise_exception=False):
        try:
            if self.helper.misc.system.py_version <= 2:
                return long(a) if a else long(0)
            else:
                return int(a) if a else 0

        except ValueError as e:
            if raise_exception:
                raise e

            return False

    def float(self, a, raise_exception=False):
        try:
            return float(a) if a else 0

        except ValueError as e:
            if raise_exception:
                raise e

            return False
