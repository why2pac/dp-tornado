#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from engine.helper import Helper as dpHelper

import urllib


class UrlHelper(dpHelper):
    def quote(self, s):
        return urllib.parse.quote_plus(s)