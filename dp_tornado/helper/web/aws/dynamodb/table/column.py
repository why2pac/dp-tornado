# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class ColumnHelper(dpHelper):
    @property
    def string(self):
        return 'S'

    @property
    def binary(self):
        return 'B'

    @property
    def number(self):
        return 'N'
