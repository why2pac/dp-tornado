# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class PostHelper(dpHelper):
    def raw(self, url, data=None, json=None, **kwargs):
        return self.helper.web.http.request(req_type='post', res_type='raw', url=url, data=data, json=json, **kwargs)

    def json(self, url, data=None, json=None, **kwargs):
        return self.helper.web.http.request(req_type='post', res_type='json', url=url, data=data, json=json, **kwargs)

    def text(self, url, data=None, json=None, **kwargs):
        return self.helper.web.http.request(req_type='post', res_type='text', url=url, data=data, json=json, **kwargs)

    def html(self, url, data=None, json=None, **kwargs):
        return self.helper.web.http.request(req_type='post', res_type='html', url=url, data=data, json=json, **kwargs)
