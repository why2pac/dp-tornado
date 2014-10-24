#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#

from engine.controller import Controller as dpController


class TestController(dpController):
    def get(self):
        self.finish(self.model.foo.bar.user.get_user_by_user_uuid('user_uuid'))