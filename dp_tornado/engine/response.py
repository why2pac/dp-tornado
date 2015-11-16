# -*- coding: utf-8 -*-


class Response(Exception):
    def __init__(self, http_status_code=200, message='An error has occurred'):
        self._http_status_code = http_status_code
        self._message = message

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