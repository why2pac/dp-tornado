# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class RandomController(Controller):
    def get(self):
        random_string = 'xxxxxxxxxx'
        random_numeric = '0000000000'

        for i in range(500):
            assert(len(self.helper.string.random.string(10)) == len(random_string))
            assert(len(self.helper.string.random.numeric(10)) == len(random_numeric))
            assert(self.helper.string.check.alphanumeric(self.helper.string.random.string(10)) is True)
            assert(self.helper.string.check.numeric(self.helper.string.random.numeric(10)) is True)

        self.finish('done')
