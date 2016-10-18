# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller
from bs4 import BeautifulSoup


class StaticController(Controller):
    def get(self):
        self.test_debug()
        self.test_local()
        self.test_path()
        self.test_s3()

        self.finish('done')

    def test_debug(self):
        self.test_files(self.render_string('tests/view/module/static/debug.html'), minified=False)

    def test_local(self):
        self.test_files(self.render_string('tests/view/module/static/local.html'), minified=True)

    def test_path(self):
        self.test_files(self.render_string('tests/view/module/static/path.html'), minified=False)

    def test_s3(self):
        self.test_files(self.render_string('tests/view/module/static/s3.html'), minified=True)

    def test_files(self, html, minified):
        o = BeautifulSoup(html, 'lxml')

        for e in o.findAll('script'):
            self.test_script(e.attrs['src'], minified=minified)

        for e in o.findAll('link'):
            self.test_css(e.attrs['href'], minified=minified)

    def test_script(self, path, minified):
        content = self.get_content(path)
        self.test_content('js', content, minified)

    def test_css(self, path, minified):
        content = self.get_content(path)
        self.test_content('css', content, minified)

    def test_content(self, ext, content, minified):
        content_valid = []

        for e in content.split('\n'):
            e = e.strip()

            if e:
                content_valid.append(e)

        if minified:
            assert(len(content_valid) == 1)
        else:
            assert(len(content_valid) > 1)

        content = '\n'.join(content_valid)

        if ext == 'js':
            assert content.startswith('js_') is True
        elif ext == 'css':
            assert content.startswith('css_') is True
        else:
            assert False

    def get_content(self, path):
        if path.startswith('/'):
            path = '%s://%s%s' % (self.request.protocol, self.request.host, path)

        code, content = self.helper.web.http.get.text(path)

        assert code == 200

        return content
