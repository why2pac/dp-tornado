# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.12.17
#


from engine.config import Config as dpConfig


class CacheConfig(dpConfig):
    def index(self):
        self.caches = {
            'store': {'driver': 'memory'},
            'memory': {'driver': 'memory', 'pure': True}
        }