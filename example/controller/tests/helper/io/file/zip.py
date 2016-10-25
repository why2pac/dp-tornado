# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class ZipController(Controller):
    def get(self):
        dir_tree = [
            'zip/foo',
            'zip/foo/bar',
            'zip/foo/bar/baz',
            'zip/bar',
            'zip/baz',
            'zip',
            'zip_test'
        ]

        self.helper.io.file.remove(dir_tree)

        for d in dir_tree:
            assert self.helper.io.file.mkdir(d)

        file_tree = [
            ('%s/foo.bar' % dir_tree[0], 'this is file, foo.bar'),
            ('%s/bar.baz' % dir_tree[1], 'this is file, bar.baz'),
            ('%s/foo.baz' % dir_tree[2], 'this is file, foo.baz'),
            ('%s/baz.foo' % dir_tree[3], 'this is file, baz.foo')
        ]

        for f in file_tree:
            self.helper.io.file.write(f[0], f[1])
            assert self.helper.io.file.is_file(f[0])

        zip_files = [
            file_tree[2][0],
            (file_tree[3][0], 'foo.baz.rename'),
            (file_tree[3][0], 'move/baz.foo.rename'),
            dir_tree[0]
        ]

        zip_archive = '%s/dp_test.zip' % dir_tree[-1]
        zip_unarchive = '%s/dp_test_unarchive' % dir_tree[-1]

        self.helper.io.file.zip.archive(destfile=zip_archive, srcfiles=zip_files)
        self.helper.io.file.zip.unarchive(srcfile=zip_archive, destpath=zip_unarchive)

        assert len(self.helper.io.file.browse(zip_unarchive)) == 3
        assert self.helper.io.file.remove(dir_tree)

        self.finish('done')
