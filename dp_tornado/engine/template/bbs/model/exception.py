# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class ExceptionModel(dpModel):
    def delegate(self, level, msg, traceback):
        print(level)
        print(msg)
        print(traceback)
