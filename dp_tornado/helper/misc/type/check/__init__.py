# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class CheckHelper(dpHelper):
    def numeric(self, val):
        return True if isinstance(val, self.helper.misc.type.numeric) else False

    def string(self, val):
        return True if isinstance(val, self.helper.misc.type.string) else False

    def array(self, val):
        return True if isinstance(val, self.helper.misc.type.array) else False

    def dict(self, val):
        return True if isinstance(val, self.helper.misc.type.dict) else False
