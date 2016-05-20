# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class StatusModel(dpModel):
    def key(self, key):
        return 'assets:status:%s' % key

    def get(self, key):
        return self.cache.get(self.key(key), dsn_or_conn='foo.bar/memory')

    def set(self, key, status, a=None, b=None, c=None, d=None):
        sets = {
            's': status,
            'e': {
                'a': a,
                'b': b,
                'c': c,
                'd': d
            }
        }

        sets = self.helper.json.serialize(sets)

        return self.cache.set(self.key(key), sets, dsn_or_conn='foo.bar/memory', expire_in=3600*2)
