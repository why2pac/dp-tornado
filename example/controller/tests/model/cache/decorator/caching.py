# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class CachingController(Controller):
    def get(self):
        foo = 'foo'
        bar = 'bar'
        baz = 'baz'

        # cache

        a1 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        b1 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        c1 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, baz)
        d1 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(bar, baz)

        assert a1 == b1
        assert a1 != c1
        assert a1 != d1
        assert c1 != d1

        self.model.tests.model_test.decorator_test.clear_cached_method_multiple_drivers()

        # after clear cached

        a2 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        b2 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        c2 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, baz)
        d2 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(bar, baz)

        assert a1 != a2
        assert b1 != b2
        assert c1 != c2
        assert d1 != d2

        assert a2 == b2
        assert a2 != c2
        assert a2 != d2
        assert c2 != d2

        ar = self.model.tests.model_test.decorator_test.renew_cached_method_multiple_drivers(foo, bar)

        a3 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        b3 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        c3 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, baz)
        d3 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(bar, baz)

        assert ar == a3
        assert ar == b3
        assert a3 == b3
        assert a3 != c3
        assert a3 != d3
        assert c3 != d3

        assert a2 != a3
        assert b2 != b3
        assert c2 == c3
        assert d2 == d3

        # cache (flush each redis db)

        a4 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        b4 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        c4 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, baz)
        d4 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(bar, baz)

        self.model.tests.model_test.decorator_test.flush_db_1()

        a5 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        b5 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        c5 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, baz)
        d5 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(bar, baz)

        assert a4 == a5
        assert b4 == b5
        assert c4 == c5
        assert d4 == d5

        a6 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        b6 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        c6 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, baz)
        d6 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(bar, baz)

        self.model.tests.model_test.decorator_test.flush_db_2()

        a7 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        b7 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        c7 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, baz)
        d7 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(bar, baz)

        assert a6 == a7
        assert b6 == b7
        assert c6 == c7
        assert d6 == d7

        a8 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        b8 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        c8 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, baz)
        d8 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(bar, baz)

        self.model.tests.model_test.decorator_test.flush_db_1()
        self.model.tests.model_test.decorator_test.flush_db_2()

        a9 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        b9 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, bar)
        c9 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(foo, baz)
        d9 = self.model.tests.model_test.decorator_test.cached_method_multiple_drivers(bar, baz)

        assert a8 != a9
        assert b8 != b9
        assert c8 != c9
        assert d8 != d9

        self.model.tests.model_test.decorator_test.clear_cached_method_multiple_drivers()

        o = self.model.tests.model_test.decorator_test.cache_method_ignore_param(foo, bar)
        p = self.model.tests.model_test.decorator_test.cache_method_ignore_param(foo, bar)
        r = self.model.tests.model_test.decorator_test.cache_method_ignore_param(foo, param2=bar)
        s = self.model.tests.model_test.decorator_test.cache_method_ignore_param(foo, param2=baz)
        t = self.model.tests.model_test.decorator_test.cache_method_ignore_param(bar, param2=foo)
        u = self.model.tests.model_test.decorator_test.cache_method_ignore_param(bar, param2=baz)

        assert o == p
        assert o != r
        assert r == s
        assert s != u
        assert t == u

        self.finish('done')
