# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class PathController(Controller):
    def get(self):
        cwd = self.helper.io.path.cwd()

        assert cwd

        browse_cwd = self.helper.io.path.browse(self.helper.io.path.cwd())

        for e in browse_cwd:
            assert e.startswith(cwd)

        browse_cwd_relative_path = self.helper.io.path.browse(self.helper.io.path.cwd(), fullpath=False)

        for e in browse_cwd_relative_path:
            assert not e.startswith(cwd)

        browse_cwd_rel_recursive = self.helper.io.path.browse(self.helper.io.path.cwd(), fullpath=False, recursive=True)

        for e in browse_cwd_rel_recursive:
            assert not e.startswith(cwd)

        browse_cwd_abs_recrusive = self.helper.io.path.browse(self.helper.io.path.cwd(), fullpath=True, recursive=True)

        for e in browse_cwd_abs_recrusive:
            assert e.startswith(cwd)

        assert len(browse_cwd) == len(browse_cwd_relative_path)
        assert len(browse_cwd_rel_recursive) == len(browse_cwd_abs_recrusive)

        assert len(browse_cwd) <= len(browse_cwd_rel_recursive)

        conds_py = {'ext': 'py'}
        browse_py = self.helper.io.path.browse(
            self.helper.io.path.cwd(), recursive=True, conditions=conds_py)

        for e in browse_py:
            assert e.endswith('.py')

        conds_py_html = {'ext': ['py', 'html']}
        browse_py_html = self.helper.io.path.browse(
            self.helper.io.path.cwd(), recursive=True, conditions=conds_py_html)

        for e in browse_py_html:
            assert e.endswith('.py') or e.endswith('.html')
