#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


import tornado.web
import tornado.ioloop
import tornado.gen
import tornado.concurrent
import tornado.options

import inspect
import importlib

from concurrent.futures import ThreadPoolExecutor
from engine.response import Response as dpResponse


class Handler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(tornado.options.options.max_worker)

    def __init__(self, application, request, **kwargs):
        super(Handler, self).__init__(application, request, **kwargs)

        self.prefix = self.prefix
        self.parent = None

        self.head_requested = False
        self.post_requested = False
        self.get_requested = False
        self.patch_requested = False
        self.delete_requested = False
        self.put_requested = False

    def initialize(self, prefix=None):
        self.prefix = prefix
    
    @staticmethod
    def capitalized_method_name(method_name):
        s = method_name.split('_')
        x = map(lambda p: p.capitalize(), s)

        return ''.join(x)

    def route(self, method, path):
        module_path = '%s.%s' % (self.prefix, path.replace('/', '.'))
        module_paths = str.split(str(module_path), '.')
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

            except ImportError:
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

            method = getattr(handler, method)

            spec = inspect.getargspec(method)
            req_param_count = len(spec.args) - 1
            def_param_count = len(spec.defaults) if spec.defaults else 0

            if len(parameters) > req_param_count or req_param_count > len(parameters) + def_param_count:
                self.finish_with_error(404, 'Page Not Found (Parameters are mismatched)')

                return False

            parameters.reverse()

            try:
                method(*parameters)
                return True

            except tornado.web.HTTPError as e:
                raise e

            except dpResponse as e:
                self.finish(e.response())
                return False

            except Exception as e:
                import traceback

                print(e)
                print(traceback.print_exc())

                # TODO, Logging

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

        self.set_status(status_code)
        self.finish('%s, %s' % (status_code, error.reason if error and error.reason else 'An error has occurred'))

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def head(self, path=None):
        yield self.__head(path)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, path=None):
        yield self.__get(path)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, path=None):
        yield self.__post(path)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def delete(self, path=None):
        yield self.__delete(path)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def patch(self, path=None):
        yield self.__patch(path)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def put(self, path=None):
        yield self.__put(path)

    @tornado.concurrent.run_on_executor
    def __head(self, path=None):
        if path and not self.head_requested:
            self.head_requested = True
            self.route('head', path)

        else:
            self.route_index()

    @tornado.concurrent.run_on_executor
    def __get(self, path=None):
        if path and not self.get_requested:
            self.get_requested = True
            self.route('get', path)

        else:
            self.route_index()

    @tornado.concurrent.run_on_executor
    def __post(self, path=None):
        if path and not self.post_requested:
            self.post_requested = True
            self.route('post', path)

        else:
            self.route_index()

    @tornado.concurrent.run_on_executor
    def __delete(self, path=None):
        if path and not self.delete_requested:
            self.delete_requested = True
            self.route('delete', path)

        else:
            self.route_index()

    @tornado.concurrent.run_on_executor
    def __patch(self, path=None):
        if path and not self.patch_requested:
            self.patch_requested = True
            self.route('patch', path)

        else:
            self.route_index()

    @tornado.concurrent.run_on_executor
    def __put(self, path=None):
        if path and not self.put_requested:
            self.put_requested = True
            self.route('put', path)

        else:
            self.route_index()

    @staticmethod
    def get_cdn_prefix():
        return ''

    def get_user_agent(self, parsed=True):
        if not parsed:
            return self.request.headers["User-Agent"]

        else:
            from plugin import http_agent_parser

            ua = self.get_user_agent(False)
            ua = http_agent_parser.detect(ua)

            platform = 'platform-%s-%s' % (ua['platform']['name']
                                           if 'platform' in ua and 'name' in ua['platform'] else 'Unknown',
                                           ua['platform']['version']
                                           if 'platform' in ua and 'version' in ua['platform'] else 'Unknown')
            platform = platform.lower().replace(' ', '-').replace('.', '-')

            os = 'os-%s-%s' % (ua['os']['name']
                               if 'os' in ua and 'name' in ua['os'] else 'Unknown',
                               ua['os']['version']
                               if 'os' in ua and 'version' in ua['os'] else 'Unknown')
            os = os.lower().replace(' ', '-').replace('.', '-')

            browser = 'browser-%s-%s' % (ua['browser']['name']
                                         if 'browser' in ua and 'name' in ua['browser'] else 'Unknown',
                                         ua['browser']['version']
                                         if 'browser' in ua and 'version' in ua['browser'] else 'Unknown')
            browser = browser.lower().replace(' ', '-').replace('.', '-')

            browser_major = 'browser-%s-%s' % (ua['browser']['name']
                                               if 'browser' in ua and 'name' in ua['browser'] else 'Unknown',
                                               int(float(ua['browser']['version'].split('.')[0]))
                                               if 'browser' in ua and 'version' in ua['browser'] else 'Unknown')
            browser_major = browser_major.lower().replace(' ', '-').replace('.', '-')

            browser_type = 'browser-%s' % (ua['browser']['name']
                                           if 'browser' in ua and 'name' in ua['browser'] else 'Unknown')
            browser_type = browser_type.lower().replace(' ', '-').replace('.', '-')

            ua['platform_str'] = platform
            ua['os_str'] = os
            ua['browser_str'] = browser
            ua['browser_major_str'] = browser_major
            ua['browser_type_str'] = browser_type

            return ua