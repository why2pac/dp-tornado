# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class CheckHelper(dpHelper):
    def exist_repeated_text(self, s, criteria=3):
        if not self.helper.misc.type.check.string(s):
            return False

        k = s[0]
        n = 0

        for c in s:
            if c == k:
                n += 1

                if n >= criteria:
                    return True

            else:
                k = c
                n = 1

        return False

    def alphanumericpunc(self, s, add=None):
        return self._check(
            s, self.helper.string.digits + self.helper.string.ascii_letters + self.helper.string.punctuation, add)

    def alphanumeric(self, s, add=None):
        return self._check(s, self.helper.string.digits + self.helper.string.ascii_letters, add)

    def alphabet(self, s, add=None):
        return self._check(s, self.helper.string.ascii_letters, add)

    def numeric(self, s, add=None):
        return self._check(s, self.helper.string.digits, add)

    def _check(self, s, criteria, add):
        if not self.helper.misc.type.check.string(s):
            return False

        add = add if add else ''
        v = any(char not in set(c for c in criteria + add) for char in s)
        return True if not v else False
