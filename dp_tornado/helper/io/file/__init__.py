# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper

import shutil
import os


class FileHelper(dpHelper):
    def remove(self, files_or_dirs=None, files=None, dirs=None):
        assert not files_or_dirs or not files or not dirs

        files_or_dirs = files_or_dirs or []
        files = files or []
        dirs = dirs or []

        if not isinstance(files_or_dirs, (list, tuple)):
            files_or_dirs = (files_or_dirs, )

        if not isinstance(files, (list, tuple)):
            files = (files, )

        if not isinstance(dirs, (list, tuple)):
            dirs = (dirs, )

        for f in files_or_dirs:
            if os.path.isdir(f):
                dirs.append(f)
            elif os.path.isfile(f):
                files.append(f)

        removed = []

        for f in files:
            if os.path.isfile(f):
                os.remove(f)
                removed.append(f)

        for f in dirs:
            if os.path.isdir(f):
                shutil.rmtree(f)
                removed.append(f)

        return removed

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

    def write(self, path, content, mode='w'):
        with open(path, mode) as fp:
            fp.write(content)

    def explore(self, path):
        return [os.path.join(path, e) for e in os.listdir(path)]

    def is_dir(self, path):
        return True if os.path.isdir(path) else False

    def is_file(self, path):
        return True if os.path.isfile(path) else False

    def dirname(self, path):
        return os.path.dirname(path)
