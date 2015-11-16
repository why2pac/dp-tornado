# -*- coding: utf-8 -*-


from dp_tornado.engine.engine import Engine


class Processor(Engine):
    def __init__(self, timeout=None):
        pass

    def run(self):
        raise NotImplementedError
