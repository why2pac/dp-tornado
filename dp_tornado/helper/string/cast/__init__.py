# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper

unicode_type = type(u'')


class CastHelper(dpHelper):
    def string(self, s, preserve_none=True):
        if s is None:
            return s if preserve_none else ''

        if not self.helper.misc.type.check.string(s):
            s = str(s)

        if type(s) == unicode_type:
            if self.helper.misc.system.py_version <= 2:
                return s.encode('UTF-8')
            else:
                return s
        else:
            return s

    def unicode(self, s, preserve_none=True):
        if s is None:
            return s if preserve_none else u''

        if not self.helper.misc.type.check.string(s):
            s = str(s)

        if type(s) != unicode_type:
            return s.decode('UTF-8')
        else:
            return s
