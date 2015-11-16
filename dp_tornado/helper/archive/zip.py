# -*- coding: utf-8 -*-


import zipfile

from dp_tornado.engine.helper import Helper as dpHelper


class ZipFile(object):
    def __init__(self, file, mode="r", compression=zipfile.ZIP_STORED, allowZip64=False):
        self.zipfile = zipfile.ZipFile(file=file, mode=mode, compression=compression, allowZip64=allowZip64)

    def appends(self, files, compress_type=None):
        for file in files:
            if isinstance(file, (tuple, list)):
                filename = file[0]
                arcname = file[1]
            else:
                filename = file
                arcname = None

            self.zipfile.write(filename=filename, arcname=arcname, compress_type=compress_type)

        return True

    def close(self):
        return self.zipfile.close()


class ZipHelper(dpHelper):
    def new(self, file, mode="r", compression=zipfile.ZIP_STORED, allowZip64=False):
        return ZipFile(file, mode, compression, allowZip64)
