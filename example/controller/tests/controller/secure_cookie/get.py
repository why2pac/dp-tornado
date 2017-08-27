# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class GetController(Controller):
    def get(self, k):
        val = self.secure_cookie(k)

        if k == 'predefined':
            val = self.helper.string.serialization.deserialize(val)
            assert val and val['foo'] and val['faz']

            self.finish(val['foo'])
            return

        self.finish(val or 'empty')
