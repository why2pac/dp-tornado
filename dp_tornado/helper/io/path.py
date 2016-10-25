# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper

import os


class PathHelper(dpHelper):
    def join(self, path, *paths):
        return os.path.join(path, *paths)

    def mkdir(self, path, mode=None):
        if self.is_file(path):
            path = self.dirname(path)

        try:
            kwargs = {}

            if mode:
                kwargs['mode'] = mode

            if not self.is_dir(path):
                os.makedirs(path, **kwargs)

        except Exception as e:
            self.logging.exception(e)
            pass

        return self.is_dir(path)

    def browse(self, path):
        return [os.path.join(path, e) for e in os.listdir(path)]

    def is_dir(self, path):
        return True if os.path.isdir(path) else False

    def is_file(self, path):
        return True if os.path.isfile(path) else False

    def dirname(self, path):
        return os.path.dirname(path)

    def ext(self, path, dot='.'):
        ext = os.path.splitext(path)[-1]

        return '%s%s' % (dot or '', ext[1:]) if ext else ''
