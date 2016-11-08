# -*- coding: utf-8 -*-


import importlib
import tornado.gen
import tornado.concurrent

from dp_tornado.engine.handler import Handler


class DpIdentifierHandler(Handler):
    def get(self, path=None):
        if self.remote_ip != '127.0.0.1':
            return self.finish_with_error(404)

        self.finish(self.ini.server.identifier or 'none')
