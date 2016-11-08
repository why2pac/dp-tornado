# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class JsonHelper(dpHelper):
    def dump(self, a, b):
        """
            .. test::
                expect(
                    json={
                        'a': 1,
                        'b': 9
                    },
                    args=(1, 9))
                expect(
                    json={
                        'b': 'abc',
                        'a': '한글'
                    },
                    args=('한글', 'abc'))
                !expect(int=11, args=(1, 9))
                !expect(str='10', args=(1, 9))
                !expect(bool=False, args=(1, 9))
        """
        return {
            'a': a,
            'b': b
        }
