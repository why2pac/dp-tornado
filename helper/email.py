# -*- coding: utf-8 -*-
#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.11.04
#


from engine.helper import Helper as dpHelper


class EmailHelper(dpHelper):
    def validate(self, e):
        return self.helper.validator.email.validate(e)