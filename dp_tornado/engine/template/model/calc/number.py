# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class NumberModel(dpModel):
    def add(self, a, b):
        return a + b
