#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		

from .handler import Handler as dpHandler
from .engine import Engine as dpEngine
from .model import InValueModelConfig as dpInValueModelConfig


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

        self._sessionid = None
        self._sessiondb = dpInValueModelConfig(driver='sqlite', database='session')

    @property
    def remote_ip(self):
        return self.request.remote_ip

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

    def get_sessionid(self):
        return self._sessionid if self._sessionid else self.set_sessionid()

    def set_sessionid(self, sessionid=None):
        if not sessionid:
            sessionid_from_cookie = self.get_secure_cookie('PSESSIONID')
            sessionid = sessionid_from_cookie

        sessionid = sessionid or self.helper.crypto.md5_hash(self.helper.datetime.current_time_millis())
        self.set_secure_cookie('PSESSIONID', sessionid)
        self._sessionid = sessionid

        return sessionid

    def get_session_value(self, name):
        sessionid = self.get_sessionid()
        key = '%s_%s' % (sessionid, name)

        return self.cache.get(key, self._sessiondb)

    def set_session_value(self, name, value):
        sessionid = self.get_sessionid()
        key = '%s_%s' % (sessionid, name)

        return self.cache.set(key, value, self._sessiondb, expire_in=3600*24*31)

    def session(self, name, value=None):
        if value is not None:
            return self.set_session_value(name, value)

        else:
            return self.get_session_value(name)

    def redirect(self, url, permanent=False, status=None):
        self.parent.redirect(url, permanent, status)

    def render(self, template_name, kwargs=None):
        self._render = {'t': template_name, 'k': kwargs}

    def render_string(self, template_name, kwargs=None):
        if kwargs:
            return self.view.render_string(self, template_name, kwargs)
        else:
            return self.view.render_string(self, template_name)

    def write(self, chunk):
        self._write.append(chunk)

    def finish(self, chunk=None):
        self._finish = chunk