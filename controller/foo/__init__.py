#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#

from engine.controller import Controller as dpController


class FooController(dpController):
    def get(self):
        params = {
            'foo': 'bar'
        }

        self.render('foo/index.html', params)