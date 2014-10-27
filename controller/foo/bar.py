#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#

from engine.controller import Controller as dpController


class BarController(dpController):
    # URL matching with /foo/bar, foo/bar/val1, foo/bar/val1/val2
    def get(self, a=None, b=None):
        self.finish('bar controller (%s, %s)' % (a, b))