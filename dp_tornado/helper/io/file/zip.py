# -*- coding: utf-8 -*-


import zipfile

from dp_tornado.engine.helper import Helper as dpHelper


class ZipHelper(dpHelper):
    def archive(self, destfile, srcfiles, mode='w', compression=zipfile.ZIP_STORED, allowZip64=False):
        archive = zipfile.ZipFile(file=destfile, mode=mode, compression=compression, allowZip64=allowZip64)

        if not isinstance(srcfiles, (list, tuple)):
            srcfiles = (srcfiles, )

        for srcfile in srcfiles:
            arcname = None
            compress_type = None

            if isinstance(srcfile, (tuple, list)):
                filename = srcfile[0]
                arcname = srcfile[1] if len(srcfile) > 1 else arcname
                compress_type = srcfile[2] if len(srcfile) > 2 else compress_type

            else:
                filename = srcfile

            self._archive_append(archive, filename, arcname, compress_type)

        archive.close()

        return True

    def _archive_append(self, archive, path, arcname, compress_type):
        if self.helper.io.path.is_file(path):
            archive.write(filename=path, arcname=arcname, compress_type=compress_type)
        elif self.helper.io.path.is_dir(path):
            for e in self.helper.io.path.browse(path):
                self._archive_append(archive=archive, path=e, arcname=arcname, compress_type=compress_type)

    def unarchive(self, srcfile, destpath, mode='r', compression=zipfile.ZIP_STORED, allowZip64=False):
        with zipfile.ZipFile(file=srcfile, mode=mode, compression=compression, allowZip64=allowZip64) as archive:
            archive.extractall(destpath)

        return True
