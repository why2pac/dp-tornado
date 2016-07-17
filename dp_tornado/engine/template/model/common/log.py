# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class LogModel(dpModel):
    def exception_delegate(self, level, msg, traceback):
        print('-------------------------------')
        print(level)
        print(msg)
        print(traceback)
