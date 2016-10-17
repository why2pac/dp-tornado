# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class RandomHelper(dpHelper):
    def int(self, length):
        return self.helper.misc.random.numeric(length)

    def range(self, minval, maxval):
        if not self.helper.misc.type.check.numeric(minval) or not self.helper.misc.type.check.numeric(maxval):
            return False

        return self.helper.misc.random.randint(minval, maxval)
