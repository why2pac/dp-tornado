# -*- coding: utf-8 -*-


import importlib
import tornado.gen
import tornado.concurrent

from dp_tornado.engine.handler import Handler


class SchedulerHandler(Handler):
    @property
    def executor(self):
        return self._executor('worker')

    def _set_response(self, plain):
        setattr(self, '__response', plain)

    def _get_response(self):
        return getattr(self, '__response', None)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, path=None):
        yield self.get_process(path=path)

        res = self._get_response()

        if res:
            self.finish(res)

    @tornado.concurrent.run_on_executor
    def get_process(self, path):
        if path == 'ping':
            self._set_response('pong')
            return

        try:
            module = importlib.import_module(path)
            runner = getattr(module, 'Scheduler')()
            runner.run()

        except Exception as e:
            self.logging.exception(e)
