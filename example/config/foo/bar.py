# -*- coding: utf-8 -*-


from dp_tornado.engine.config import Config


class BarConfig(Config):
    def index(self):
        self.conf.databases = {
            'bar': {'driver': 'sqlite'},
            'local': {'driver': 'sqlite'},
            'schema': {
                'driver': 'mysql+cymysql',
                'database': 'dev',
                'host': '127.0.0.1',
                'port': 3306,
                'user': 'root',
                'password': 'drg@mysql',
                'pool_size': 1,
                'charset': 'utf8'
            }
        }

        self.conf.caches = {
            'memory': {'driver': 'memory'}
        }
