# -*- coding: utf-8 -*-


import importlib
import tornado.gen
import tornado.concurrent

from dp_tornado.engine.handler import Handler


class SchedulerHandler(Handler):
    @property
    def executor(self):
        return self._executor('worker')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, path=None):
        yield self.get_process(path=path)

    @tornado.concurrent.run_on_executor
    def get_process(self, path):
        try:
            module = importlib.import_module(path)
            runner = getattr(module, 'Scheduler')()
            runner.run()

        except Exception as e:
            self.logging.exception(e)
