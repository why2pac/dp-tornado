#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.28
#


class Response(Exception):
    def __init__(self, message=None, http_status_code=None):
        self._http_status_code = http_status_code if http_status_code else 200
        self._message = message if message else 'An error has occurred'

    @property
    def http_status_code(self):
        return self._http_status_code

    @property
    def message(self):
        return self._message

    def __str__(self):
        return '%s %s' % (self.http_status_code, self.message)

    def response(self):
        return str(self)