# -*- coding: utf-8 -*-


from dp_tornado.engine.config import Config as dpConfig


class VersionConfig(dpConfig):
    def index(self):
        self.conf.master = '1.0'
