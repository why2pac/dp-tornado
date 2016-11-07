# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class JsonModel(dpModel):
    def dump(self, a, b):
        """
            .. test::
                expect(
                    json={
                        'a': 1,
                        'b': 9
                    },
                    args=(1, 9))
                !expect(int=11, args=(1, 9))
                !expect(str='10', args=(1, 9))
                !expect(bool=False, args=(1, 9))
        """
        return a + b
