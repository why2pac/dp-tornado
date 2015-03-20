# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.10.23
#


import tornado.web
import tornado.ioloop
import tornado.gen
import tornado.concurrent
import tornado.options

import inspect
import importlib

from .response import Response as dpResponse
from .engine import Engine as dpEngine
from .model import InValueModelConfig as dpInValueModelConfig


session_default_expire_in = tornado.options.options.session_expire_in or 7200


class Handler(tornado.web.RequestHandler, dpEngine):
    executor = tornado.concurrent.futures.ThreadPoolExecutor(tornado.options.options.max_worker)

    def __init__(self, application, request, **kwargs):
        super(Handler, self).__init__(application, request, **kwargs)

        self.prefix = self.prefix
        self.parent = None
        self.routed = None
        self.blocked = False

        session_dsn = tornado.options.options.session_dsn

        self._sessionid = None
        self._sessiondb = session_dsn or dpInValueModelConfig(driver='sqlite', database='session')

    def initialize(self, prefix=None):
        self.prefix = prefix

    @staticmethod
    def capitalized_method_name(method_name):
        s = method_name.split('_')
        x = map(lambda p: p.capitalize(), s)

        return ''.join(x)

    @tornado.concurrent.run_on_executor
    def route(self, method, path):
        if self.blocked:
            self.finish_with_error(404, 'Page Not Found')
            return False

        module_path = '%s.%s' % (self.prefix, path.replace('/', '.'))
        module_paths = str.split(self.helper.string.to_str(module_path), '.')
        parameters = []
        previous = None

        if module_paths[-1].strip() == '':
            module_paths.pop()

        while True:
            if len(module_paths) == 0:
                break

            module_path = '.'.join(module_paths)
            pop = module_paths.pop()
            class_name = '%sController' % (self.capitalized_method_name(pop))
            handler_module = None

            if module_path == self.prefix:
                break

            try:
                handler_module = importlib.import_module(module_path)
                handler = getattr(handler_module, class_name)
                handler = handler(self.application, self.request, prefix=self.prefix, parent=self)
                handler.prefix = self.prefix
                handler.parent = self

            except (KeyError, ValueError, AttributeError, ImportError):
                try:
                    class_name = '%sController' % (self.capitalized_method_name(previous))
                    handler = getattr(handler_module, class_name)
                    handler = handler(self.application, self.request, prefix=self.prefix, parent=self)

                    # Its handler.
                    parameters.pop()

                except AttributeError:
                    previous = pop
                    parameters.append(pop)
                    continue

            method = getattr(handler, method, None)

            if not method:
                self.finish_with_error(404, 'Page Not Found (No Method Implemented)')

            spec = inspect.getargspec(method)
            req_param_count = len(spec.args) - 1
            def_param_count = len(spec.defaults) if spec.defaults else 0

            if len(parameters) > req_param_count or req_param_count > len(parameters) + def_param_count:
                self.finish_with_error(404, 'Page Not Found (Parameters are mismatched)')

                return False

            parameters.reverse()

            try:
                method(*parameters)
                return handler

            except tornado.web.HTTPError as e:
                raise e

            except dpResponse as e:
                self.set_status(e.http_status_code)
                self.finish(e.response())

                return handler

            except Exception as e:
                self.logger.exception(e)
                self.finish_with_error(500)

                return False

        self.finish_with_error(404, 'Page Not Found')

        return False

    def route_index(self):
        try:
            index_method = getattr(self, 'index')
        except AttributeError:
            raise tornado.web.HTTPError(404)

        try:
            return index_method()
        except Exception:
            raise tornado.web.HTTPError(500)

    @staticmethod
    def finish_with_error(status_code, message='An error has occurred'):
        raise tornado.web.HTTPError(status_code, reason=message)

    def write_error(self, status_code, **kwargs):
        error = kwargs.get('exc_info', None)
        error = error[1] if error else None
        reason = error.reason if error and getattr(error, 'reason', None) else 'An error has occurred'
        finish = '%s, %s' % (status_code, reason)

        self.set_status(status_code)
        self.finish(finish)

    def head(self, path=None):
        if path and not self.routed:
            self.routed = True
            self.__head(path)
        else:
            self.routed = False
            self.route_index()

    def get(self, path=None):
        if path and not self.routed:
            self.routed = True
            self.__get(path)
        else:
            self.routed = False
            self.route_index()

    def post(self, path=None):
        if path and not self.routed:
            self.routed = True
            self.__post(path)
        else:
            self.routed = False
            self.route_index()

    def delete(self, path=None):
        if path and not self.routed:
            self.routed = True
            self.__delete(path)
        else:
            self.routed = False
            self.route_index()

    def patch(self, path=None):
        if path and not self.routed:
            self.routed = True
            self.__patch(path)
        else:
            self.routed = False
            self.route_index()

    def put(self, path=None):
        if path and not self.routed:
            self.routed = True
            self.__put(path)
        else:
            self.routed = False
            self.route_index()

    def __render(self, x):
        if not x._render:
            return

        t = x._render['t']
        k = x._render['k']

        if not k:
            self.render(t)
        else:
            self.render(t, **k)

    def __write(self, x):
        if not x._write:
            return

        for s in x._write:
            self.write(s)

    def __finish(self, x):
        if not x._finish:
            return

        self.finish(x._finish)

    def postprocess(self, x):
        if x._render:
            self.__render(x)
        elif x._finish:
            self.__finish(x)
        elif x._write:
            self.__write(x)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def __head(self, path=None):
        x = yield self.route('head', path)
        self.postprocess(x)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def __get(self, path=None):
        x = yield self.route('get', path)
        self.postprocess(x)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def __post(self, path=None):
        x = yield self.route('post', path)
        self.postprocess(x)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def __delete(self, path=None):
        x = yield self.route('delete', path)
        self.postprocess(x)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def __patch(self, path=None):
        x = yield self.route('patch', path)
        self.postprocess(x)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def __put(self, path=None):
        x = yield self.route('put', path)
        self.postprocess(x)

    @property
    def remote_ip(self):
        return self.request.headers['X-Forwarded-For'] \
            if 'X-Forwarded-For' in self.request.headers else self.request.remote_ip

    def set_secure_cookie(self, name, value, expires_days=30, version=2, **kwargs):
        secure_cookie = self.helper.crypto.encrypt(value, True, 0, self.request.headers["User-Agent"])
        return super(Handler, self).set_secure_cookie(name, secure_cookie, expires_days, version, **kwargs)

    def get_secure_cookie(self, name, value=None, max_age_days=31, min_version=None):
        secure_cookie = super(Handler, self).get_secure_cookie(name, value, max_age_days, min_version)

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
            try:
                sessionid_from_cookie = self.get_secure_cookie('PSESSIONID')
                sessionid = self.helper.string.to_str(sessionid_from_cookie)

                if not sessionid.isalnum():
                    sessionid = None

            except:
                sessionid = None

        sessionid = sessionid or self.helper.crypto.sha224_hash(self.helper.datetime.current_time_millis())
        self.set_secure_cookie('PSESSIONID', sessionid)
        self._sessionid = sessionid

        return sessionid

    def get_session_value(self, name, expire_in=None):
        sessionid = self.get_sessionid()
        key = '%s:%s' % (sessionid, name)

        return self.cache.get(key, self._sessiondb, expire_in=expire_in)

    def set_session_value(self, name, value, expire_in=session_default_expire_in):
        sessionid = self.get_sessionid()
        key = '%s:%s' % (sessionid, name)

        return self.cache.set(key, value, self._sessiondb, expire_in=expire_in)

    def session(self, name, value=None, expire_in=session_default_expire_in):
        if value is not None:
            return self.set_session_value(name, value, expire_in=expire_in)

        else:
            return self.get_session_value(name)