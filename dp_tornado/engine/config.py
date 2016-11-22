# -*- coding: utf-8 -*-
"""Here is a `foo_bar` config example:

.. testcode::

    from dp_tornado.engine.config import Config


    class FooBarConfig(Config):
        def index(self):
            self.conf.value_str = 'string'
            self.conf.value_int = 10
            self.conf.value_dict = {
                'foo': 100,
                'bar': {
                    'baz': 200,
                    'baf': 300
                }
            }

            self.conf.databases = {
                'drv_sqlite_name': {
                    'driver': 'sqlite'
                },
                'drv_mysql_name': {
                    'driver': 'mysql+cymysql',
                    'database': '',
                    'host': '127.0.0.1',
                    'port': 3306,
                    'user': 'root',
                    'password': '',
                    'pool_size': 1,
                    'charset': 'utf8'
                }
            }

            self.conf.caches = {
                'drv_sqlite_name': {
                    'driver': 'memory',
                    'identifier': 'dp_test_sqlite'
                },
                'drv_redis_name': {
                    'driver': 'redis',
                    'host': '127.0.0.1',
                    'port': 6379,
                    'password': None,
                    'maxconn': 256
                }
            }


File/Class Invoke rules
-----------------------
* */config/__init__.py*, **DO NOT IMPLEMENT ANY CODE IN THIS FILE**
* */config/blog/__init__.py*, ``BlogConfig`` > **config.blog**
* */config/blog/admin/__init__.py*, ``AdminConfig`` > **config.blog.admin**
* */config/blog/post.py*, ``PostConfig`` > **config.blog.post**
* */config/blog/view.py*, ``ViewConfig`` > **config.blog.view**
* */config/foo_bar.py*, ``FooBarConfig`` > **config.foo_bar**


Config Invoke rules
-------------------
* */config/foo_bar.py*, ``self.conf.value_str``: **config.foo_bar.value_str == 'string'**
* */config/foo_bar.py*, ``self.conf.value_int``: **config.foo_bar.value_int == 10**
* */config/foo_bar.py*, ``self.conf.value_dict``: **config.foo_bar.value_dict.foo == 100**
* */config/foo_bar.py*, ``self.conf.value_dict``: **config.foo_bar.value_dict.bar.baz == 200**
* */config/foo_bar.py*, ``self.conf.value_dict``: **config.foo_bar.value_dict.bar.baf == 300**
* */config/foo_bar.py*, ``self.conf.databases``: **'foo_bar/drv_sqlite_name'**
* */config/foo_bar.py*, ``self.conf.databases``: **'foo_bar/drv_mysql_name'**
* */config/foo_bar.py*, ``self.conf.databases``: **'foo_bar/drv_sqlite_name'**
* */config/foo_bar.py*, ``self.conf.databases``: **'foo_bar/drv_redis_name'**
"""


from .singleton import Singleton as dpSingleton
from .namer import Namer as dpNamer
from .loader import Loader as dpLoader
from .engine import EngineSingleton as dpEngineSingleton


engine = dpEngineSingleton()


class Config(dpLoader, dpSingleton):
    conf = dpNamer()

    def __getattr__(self, name):
        return self.__getattr_inner__(name) or self.conf.__getattr__(name)

    @property
    def ini(self):
        return engine.ini
