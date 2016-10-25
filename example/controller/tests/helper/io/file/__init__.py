# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class FileController(Controller):
    def get(self):
        dir_tree = [
            'foo/bar/baz'
            'bar',
            'bar/foo',
            'baz'
        ]

        self.helper.io.file.remove(dir_tree)

        for d in dir_tree:
            assert self.helper.io.path.mkdir(d)

        assert self.helper.io.file.remove(dir_tree)

