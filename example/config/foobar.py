# -*- coding: utf-8 -*-


from dp_tornado.engine.config import Config


class FoobarConfig(Config):
    def index(self):
        self.databases = {
            'bar': {'driver': 'sqlite'},
            'local': {'driver': 'sqlite'}
        }