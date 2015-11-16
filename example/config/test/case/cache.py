# -*- coding: utf-8 -*-


from dp_tornado.engine.config import Config


class CacheConfig(Config):
    def index(self):
        self.caches = {
            'store': {'driver': 'memory'},
            'memory': {'driver': 'memory', 'pure': True}
        }