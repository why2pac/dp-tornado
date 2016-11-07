# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class TestingModel(dpModel):
    def add(self, a, b):
        """
            .. test::
                expect(int=10, args=(1, 9))
                expect(
                    int=10,
                    kwargs={
                        'a': 1,
                        'b': 9
                    })
                !expect(int=11, args=(1, 9))
                !expect(str='10', args=(1, 9))
                !expect(bool=False, args=(1, 9))
        """
        return a + b

    def minus(self, a, b):
        """
            .. test::
                expect(int=10, args=(11, 1))
                expect(
                    int=10,
                    kwargs={
                        'a': 11,
                        'b': 1
                    })
                !expect(int=11, args=(11, 1))
                !expect(str='10', args=(11, 1))
                !expect(bool=False, args=(1, 9))
        """
        return a - b