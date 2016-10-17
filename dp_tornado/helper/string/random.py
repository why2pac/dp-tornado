# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class RandomHelper(dpHelper):
    def string(self, length):
        return ''.join(self.helper.misc.random.sample(self.helper.string.ascii_letters, length))

    def numeric(self, length):
        return ''.join(self.helper.misc.random.sample(self.helper.string.digits, length))
