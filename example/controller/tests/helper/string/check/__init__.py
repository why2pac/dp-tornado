# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class CheckController(Controller):
    def get(self):
        assert(self.helper.string.check.exist_repeated_text(1234567890, 2) is False)
        assert(self.helper.string.check.exist_repeated_text('aaa1234567890', 2) is True)
        assert(self.helper.string.check.exist_repeated_text('aaa1234567890', 3) is True)

        assert(self.helper.string.check.alphanumericpunc(1234567890) is False)
        assert(self.helper.string.check.alphanumericpunc('abc123!@#') is True)
        assert(self.helper.string.check.alphanumericpunc('abc') is True)
        assert(self.helper.string.check.alphanumericpunc('123') is True)
        assert(self.helper.string.check.alphanumericpunc('!@#') is True)
        assert(self.helper.string.check.alphanumericpunc('abc123') is True)
        assert(self.helper.string.check.alphanumericpunc('abc!@#') is True)
        assert(self.helper.string.check.alphanumericpunc('123!@#') is True)

        assert(self.helper.string.check.alphanumeric(1234567890) is False)
        assert(self.helper.string.check.alphanumeric('abc123!@#') is False)
        assert(self.helper.string.check.alphanumeric('abc') is True)
        assert(self.helper.string.check.alphanumeric('123') is True)
        assert(self.helper.string.check.alphanumeric('!@#') is False)
        assert(self.helper.string.check.alphanumeric('abc123') is True)
        assert(self.helper.string.check.alphanumeric('abc!@#') is False)
        assert(self.helper.string.check.alphanumeric('123!@#') is False)

        assert(self.helper.string.check.alphabet(1234567890) is False)
        assert(self.helper.string.check.alphabet('abc123!@#') is False)
        assert(self.helper.string.check.alphabet('abc') is True)
        assert(self.helper.string.check.alphabet('123') is False)
        assert(self.helper.string.check.alphabet('!@#') is False)
        assert(self.helper.string.check.alphabet('abc123') is False)
        assert(self.helper.string.check.alphabet('abc!@#') is False)
        assert(self.helper.string.check.alphabet('123!@#') is False)

        assert(self.helper.string.check.numeric(1234567890) is False)
        assert(self.helper.string.check.numeric('abc123!@#') is False)
        assert(self.helper.string.check.numeric('abc') is False)
        assert(self.helper.string.check.numeric('123') is True)
        assert(self.helper.string.check.numeric('!@#') is False)
        assert(self.helper.string.check.numeric('abc123') is False)
        assert(self.helper.string.check.numeric('abc!@#') is False)
        assert(self.helper.string.check.numeric('123!@#') is False)

        self.finish('done')
