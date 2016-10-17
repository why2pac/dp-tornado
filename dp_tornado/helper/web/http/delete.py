# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class DeleteHelper(dpHelper):
    def raw(self, url, **kwargs):
        return self.helper.web.http.request(req_type='delete', res_type='raw', url=url, **kwargs)

    def json(self, url, **kwargs):
        return self.helper.web.http.request(req_type='delete', res_type='json', url=url, **kwargs)

    def text(self, url, **kwargs):
        return self.helper.web.http.request(req_type='delete', res_type='text', url=url, **kwargs)

    def html(self, url, **kwargs):
        return self.helper.web.http.request(req_type='delete', res_type='html', url=url, **kwargs)
