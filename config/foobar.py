# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.10.28
#


from engine.config import Config as dpConfig


class FoobarConfig(dpConfig):
    def index(self):
        self.databases = {
            'bar': {'driver':'postgresql', 'database':'adtv_user', 'host':'192.168.2.102', 'port':5432, 'user':'melchi', 'password':'1234'}
        }