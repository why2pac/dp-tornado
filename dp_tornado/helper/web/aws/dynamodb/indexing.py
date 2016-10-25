# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class IndexingHelper(dpHelper):
    @property
    def partition(self):
        return self.hash

    @property
    def hash(self):
        return 'HASH'

    @property
    def sort(self):
        return self.range

    @property
    def range(self):
        return 'RANGE'
