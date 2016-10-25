# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper

import shutil
import os
import filecmp


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

    def write(self, path, content, mode='w'):
        with open(path, mode) as fp:
            fp.write(content)

    def compare(self, *files):
        if not files:
            return None

        def _iter():
            l = len(files)
            for i in range(l-1):
                yield files[i], files[i+1]

        try:
            for f1, f2 in _iter():
                if not filecmp.cmp(f1, f2):
                    return False
        except Exception as e:
            self.logging.exception(e)

            return False

        return True
