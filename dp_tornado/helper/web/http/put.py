# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class PutHelper(dpHelper):
    def raw(self, url, data=None, **kwargs):
        return self.helper.web.http.request(req_type='put', res_type='raw', url=url, data=data, **kwargs)

    def json(self, url, data=None, **kwargs):
        return self.helper.web.http.request(req_type='put', res_type='json', url=url, data=data, **kwargs)

    def text(self, url, data=None, **kwargs):
        return self.helper.web.http.request(req_type='put', res_type='text', url=url, data=data, **kwargs)

    def html(self, url, data=None, **kwargs):
        return self.helper.web.http.request(req_type='put', res_type='html', url=url, data=data, **kwargs)
