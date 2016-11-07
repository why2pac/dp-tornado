# -*- coding: utf-8 -*-


import sys

from .engine import Engine as dpEngine


class Testing(dpEngine):
    def __init__(self, app_module, path):
        self.app_module = app_module
        self.path = path

        self.tests = {}
        self.modules = {}

        for e in ('controller', 'model', 'helper'):
            self.tests[e] = []

    def traverse(self):
        for module in ('controller', 'model', 'helper'):
            if not self._traverse(module, self.helper.io.path.join(self.path, module)):
                return False

        return True

    def _traverse(self, module, path):
        for e in self.helper.io.path.browse(path, fullpath=False, recursive=True, conditions={'ext': 'py'}):
            path, cls = self.import_class(module, e)

            if cls is False:
                return False

            for m in dir(cls):
                attr = getattr(cls, m)
                docstring = attr.__doc__

                if docstring and docstring.find('.. test::') != -1:
                    def expect(alt, **kwargs):
                        self.tests[module].append((cls, m, alt, path, kwargs))

                    docstring = docstring[docstring.find('.. test::')+len('.. test::'):]
                    docstring = '\n'.join([e for e in docstring.split('\n') if e.strip()]).strip()

                    while True:
                        if docstring.find('expect(') != 0 and docstring.find('!expect(') != 0:
                            break

                        next_stmt = docstring[2:].find('expect(')

                        stmt = docstring[:next_stmt].strip() if next_stmt != -1 else docstring
                        docstring = docstring[len(stmt):].strip()

                        stmt = stmt.replace('expect(', 'expect(True, ')
                        stmt = stmt.replace('!expect(True,', 'expect(False,')

                        eval(stmt)

        return True

    def import_class(self, mod, path):
        path = path.split('.')[0].split('/')

        if path[-1] == '__init__':
            path.pop()

        if mod in ('model', 'helper') and not path:
            return path, None

        cls_name = ''.join([e.capitalize() for e in (path[-1] if path else 'starter').split('_')] + [mod.capitalize()])
        module = '.'.join([self.app_module, mod] + path)

        try:
            __import__(module)
            app = sys.modules[module] if module in sys.modules else None
            cls = getattr(app, cls_name, None)

            if not cls:
                self.logging.info('* Class load error, %s' % module)
                return path, False

            return path, cls

        except:
            self.logging.info('* File import error, %s' % module)

            return path, False

    def run(self):
        self.logging.info('*')

        for e in self.tests['controller']:
            self.logging.info(e)

        self.logging.info('*')

        for e in self.tests['model']:
            self.logging.info(e)

        self.logging.info('*')

        for e in self.tests['helper']:
            self.logging.info(e)

        self.logging.info('*')

        return False


'''

    Controller:
        expect / !exepct : code, text, json
        args : args, kwargs, params

    Model, Helper:
        expect / !exepct : int, long, bool, json
        args : args, kwargs


    Usage:
    ------

    class FooController(dpController):
        def get(self):
            """
                .. test::
                    expect(
                        code=200,
                        text='foo==bar',
                        params={'foo': 'bar'})
            """
            foo = self.get_argument('foo')

            if foo == 'bar':
                return self.finish('foo==bar')

            self.finish('done')

        def post(self):
            """
                .. test::
                    expect(code=400, params={'foo': 'bar'})
            """
            foo = self.get_argument('foo')

            if foo == 'bar':
                return self.finish_with_error(400)

            self.finish('done')

    class FooController(dpController):
        def get(self):
            """
                Test with params and expect json value.

                .. test::
                    expect(json="{'foo':'bar'}", params={'foo': 'bar'})
            """
            foo = self.get_argument('foo')
            return self.finish({'foo': bar)

    class FooController(dpController):
        def get(self):
            """
                Test with params and expect json value.

                .. test::
                    expect(json={'foo':'bar'}, params={'foo': 'bar'})
            """
            foo = self.get_argument('foo')
            return self.finish({'foo': bar)

    class FooModel(dpModel):
        def foobar(self, foo):
            """
                Test with kwargs arguments.

                .. test::
                    expect(int=100, kwargs={'foo': 'bar'})
            """
            if foo == 'bar':
                return int(100)

            return 0

    class FooModel(dpModel):
        def foobar(self, foo):
            """
                Test with kwargs arguments.

                .. test::
                    expect(long=100, kwargs={'foo': 'bar'})
                    expect(long=0, kwargs={'foo': 'foo'})
                    !expect(long=0, kwargs={'foo': 'bar'})
            """
            if foo == 'bar':
                if self.e.helper.misc.system.py_version <= 2:
                    return long(100)
                else:
                    return int(100)


            if self.e.helper.misc.system.py_version <= 2:
                return long(0)
            else:
                return int(0)

    class FooHelper(dpHelper):
        def foobar(self, foo, bar):
            """
                Test with args arguments.

                .. test::
                    expect(bool=True, args={'foo': 'bar'})
                    !expect(bool=False, args={'foo': 'bar'})
            """
            foo = self.get_argument('foo')

            if foo == 'bar':
                return True

            return False

'''