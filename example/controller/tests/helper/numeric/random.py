# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class RandomController(Controller):
    def get(self):
        for i in range(5000):
            assert(1 <= self.helper.numeric.random.int(1) <= 9)
            assert(10 <= self.helper.numeric.random.int(2) <= 99)

            assert(0 <= self.helper.numeric.random.range(0, 10) <= 10)
            assert(10 <= self.helper.numeric.random.range(10, 99) <= 99)

        self.finish('done')
