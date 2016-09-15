# -*- coding: utf-8 -*-


import importlib

from dp_tornado.engine.handler import Handler


class SchedulerHandler(Handler):
    def get(self, path):
        try:
            module = importlib.import_module(path)
            runner = getattr(module, 'Scheduler')()
            runner.run()

        except Exception as e:
            self.logging.exception(e)
