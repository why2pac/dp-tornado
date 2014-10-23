# -*- coding: utf-8 -*-
#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#

from engine.handler import Handler as dpHandler

class StarterController(dpHandler):
    def index(self):
        self.finish('Welcome dp for Tornado')