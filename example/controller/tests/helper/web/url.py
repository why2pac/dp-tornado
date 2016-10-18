# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class UrlController(Controller):
    def get(self):
        assert(self.helper.web.url.validate('www.google.com') is False)
        assert(self.helper.web.url.validate('http://www.google.com') is True)
        assert(self.helper.web.url.validate('unknown://www.google.com') is False)
        assert(self.helper.web.url.validate('https://www.google.com') is True)
        assert(self.helper.web.url.validate('http://www.google.com/resource?param=value') is True)
        assert(self.helper.web.url.validate('https://10.10.10.10') is True)

        plain = '안녕하세요 abc 123 !@#'
        quoted = '%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94%20abc%20123%20%21%40%23'

        assert(self.helper.web.url.quote(plain) == quoted)
        assert(self.helper.web.url.unquote(quoted) == plain)

        url_google = 'http://www.google.com?q=val'
        url_path = '/foo/bar/path?p=1&q=2'

        pa_google = self.helper.web.url.parse(url_google)
        pa_test = self.helper.web.url.parse(self)
        pa_path = self.helper.web.url.parse(url_path)

        assert(pa_google.scheme == 'http' and pa_google.netloc == 'www.google.com' and pa_google.query['q'] == 'val')
        assert(pa_test.scheme == 'http' and pa_test.path == '/tests/helper/web/url')
        assert (pa_path.scheme == '' and pa_path.path == '/foo/bar/path')

        pa_path_re = self.helper.web.url.parse(pa_path.build())

        assert(pa_path == pa_path_re)

        bu_google = self.helper.web.url.build(url_google, {'foo': 'bar*'})
        bu_google_url = 'http://www.google.com?q=val&foo=bar%2A'

        bu_google_pa = self.helper.web.url.parse(bu_google)
        bu_google_pa_url = self.helper.web.url.parse(bu_google_url)

        assert(bu_google_pa == bu_google_pa_url)

        bu_google_pa_url = self.helper.web.url.build(bu_google_pa, {'foo': 'baz'})
        pa_google_pa_url = self.helper.web.url.parse(bu_google_pa_url)

        assert(pa_google_pa_url.query['foo'] == 'baz')

        self.finish('done')
