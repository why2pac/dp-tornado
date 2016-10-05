# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class TestsModel(dpModel):
    def assert_tuple(self, a, b, comp=True):
        if comp is True:
            if list(a) != list(b):
                print('A > %s' % list(a))
                print('B > %s' % list(b))

            assert(list(a) == list(b))
        elif comp is False:
            assert(list(a) == list(b))
        else:
            assert(list(a) == comp and list(b) == comp)
