# -*- coding: utf-8 -*-


from tornado.web import StaticFileHandler


class StaticHandler(StaticFileHandler):
    def write_error(self, status_code, **kwargs):
        error = kwargs.get('exc_info', None)
        error = error[1] if error else None
        reason = error.reason if error and getattr(error, 'reason', None) else 'An error has occurred'

        self.set_status(status_code)

        if status_code == 404:
            return self.render('system/http/pp_404.html')

        return self.render('system/http/pp_5xx.html')
