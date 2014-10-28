#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		

from .handler import Handler as dpHandler
from .engine import Engine as dpEngine


class Controller(dpHandler, dpEngine):
    def initialize(self, prefix, parent=None):
        self.prefix = prefix
        self.parent = parent

        self.head_requested = False
        self.post_requested = False
        self.get_requested = False
        self.patch_requested = False
        self.delete_requested = False
        self.put_requested = False

    def set_secure_cookie(self, name, value, expires_days=30, version=2, **kwargs):
        secure_cookie = self.helper.crypto.encrypt(value, True, 0, self.request.headers["User-Agent"])
        return self.parent.set_secure_cookie(name, secure_cookie, expires_days, version, **kwargs)

    def get_secure_cookie(self, name, value=None, max_age_days=31, min_version=None):
        secure_cookie = self.parent.get_secure_cookie(name, value, max_age_days, min_version)

        if secure_cookie:
            try:
                secure_cookie = self.helper.crypto.decrypt(secure_cookie, self.request.headers["User-Agent"])
            except:
                secure_cookie = None

            return secure_cookie if secure_cookie else None

        else:
            return None

    def redirect(self, url, permanent=False, status=None):
        self.parent.redirect(url, permanent, status)

    def render(self, template_name, kwargs=None):
        if kwargs:
            self.view.render(self, template_name, kwargs)
        else:
            self.view.render(self, template_name)

    def render_string(self, template_name, kwargs=None):
        if kwargs:
            return self.view.render_string(self, template_name, kwargs)
        else:
            return self.view.render_string(self, template_name)

    def write(self, chunk):
        self.view.write(self, chunk)

    def finish(self, chunk=None):
        self.view.finish(self, chunk)