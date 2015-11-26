# -*- coding: utf-8 -*-


from dp_tornado.engine.config import Config


class BarConfig(Config):
    def index(self):
        self.conf.databases = {
            'bar': {'driver': 'sqlite'},
            'local': {'driver': 'sqlite'}
        }

        self.conf.caches = {
            'memory': {'driver': 'memory'}
        }
