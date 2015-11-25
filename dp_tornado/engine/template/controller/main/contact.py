# -*- coding: utf-8 -*-

from dp_tornado.engine.controller import Controller as dpController


class ContactController(dpController):
    def get(self, param1=None, param2=None):
        server_version = self.config.server.version.master

        self.finish('/main/contact with %s, %s (server ver. %s)' % (param1, param2, server_version))
