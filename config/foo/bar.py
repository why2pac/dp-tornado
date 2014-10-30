#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from engine.config import Config as dpConfig


class BarConfig(dpConfig):
    def index(self):
        self.databases = {
            'bar': {'driver':'postgresql', 'database':'adtv_user', 'host':'192.168.2.102', 'port':5432, 'user':'melchi', 'password':'1234'},
            'local': {'driver':'sqlite'}
        }