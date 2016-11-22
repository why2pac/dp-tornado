# -*- coding: utf-8 -*-


from dp_tornado.engine.config import Config


class DbConfig(Config):
    def index(self):
        self.conf.databases = {
            'service': {
                'driver': 'sqlite'
            }
        }
