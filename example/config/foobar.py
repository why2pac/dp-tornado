# -*- coding: utf-8 -*-


from dp_tornado.engine.config import Config


class FoobarConfig(Config):
    def index(self):
        self.conf.databases = {
            'bar': {'driver': 'sqlite'},
            'local': {'driver': 'sqlite'}
        }
