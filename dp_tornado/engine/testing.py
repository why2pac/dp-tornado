# -*- coding: utf-8 -*-


from .singleton import Singleton as dpSingleton
from .engine import Engine as dpEngine


class Testing(dpEngine, dpSingleton):
    pass


"""

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
            '''
                test:
                    expect(
                        code=200,
                        text='foo==bar',
                        params={'foo': 'bar'})
            '''
            foo = self.get_argument('foo')

            if foo == 'bar':
                return self.finish('foo==bar')

            self.finish('done')

        def post(self):
            '''
                test:
                    expect(code=400, params={'foo': 'bar'})
            '''
            foo = self.get_argument('foo')

            if foo == 'bar':
                return self.finish_with_error(400)

            self.finish('done')

    class FooController(dpController):
        def get(self):
            '''
                Test with params and expect json value.

                test:
                    expect(json="{'foo':'bar'}", params={'foo': 'bar'})
            '''
            foo = self.get_argument('foo')
            return self.finish({'foo': bar)

    class FooController(dpController):
        def get(self):
            '''
                Test with params and expect json value.

                test:
                    expect(json={'foo':'bar'}, params={'foo': 'bar'})
            '''
            foo = self.get_argument('foo')
            return self.finish({'foo': bar)

    class FooModel(dpModel):
        def foobar(self, foo):
            '''
                Test with kwargs arguments.

                test:
                    expect(int=100, kwargs={'foo': 'bar'})
            '''
            if foo == 'bar':
                return int(100)

            return 0

    class FooModel(dpModel):
        def foobar(self, foo):
            '''
                Test with kwargs arguments.

                test:
                    expect(long=100, kwargs={'foo': 'bar'})
                    expect(long=0, kwargs={'foo': 'foo'})
                    !expect(long=0, kwargs={'foo': 'bar'})
            '''
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
            '''
                Test with args arguments.

                test:
                    expect(bool=True, args={'foo': 'bar'})
                    !expect(bool=False, args={'foo': 'bar'})
            '''
            foo = self.get_argument('foo')

            if foo == 'bar':
                return True

            return False

"""