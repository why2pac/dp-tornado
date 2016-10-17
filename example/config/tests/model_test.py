# -*- coding: utf-8 -*-


from dp_tornado.engine.config import Config


class ModelTestConfig(Config):
    def index(self):
        self.conf.databases = {
            'drv_sqlite': {
                'driver': 'sqlite'
            },
            'drv_mysql_sys': {
                'driver': 'mysql+cymysql',
                'database': '',
                'host': '127.0.0.1',
                'port': 3306,
                'user': 'root',
                'password': '',
                'pool_size': 1,
                'charset': 'utf8'
            },
            'drv_mysql_test': {
                'driver': 'mysql+cymysql',
                'database': 'dp_test',
                'host': '127.0.0.1',
                'port': 3306,
                'user': 'root',
                'password': '',
                'pool_size': 1,
                'charset': 'utf8'
            }
        }

        self.conf.caches = {
            'drv_sqlite': {
                'driver': 'memory',
                'identifier': 'dp_test_sqlite'
            },
            'drv_sqlite_2': {
                'driver': 'memory',
                'identifier': 'dp_test_sqlite',
                'database': 2
            },
            'drv_redis': {
                'driver': 'redis',
                'host': '127.0.0.1',
                'port': 6379,
                'password': None,
                'maxconn': 256
            },
            'drv_redis_2': {
                'driver': 'redis',
                'database': 2,
                'host': '127.0.0.1',
                'port': 6379,
                'password': None,
                'maxconn': 256
            }
        }
