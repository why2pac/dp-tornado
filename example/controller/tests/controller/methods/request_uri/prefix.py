# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class PrefixController(Controller):
    def get(self):
        if 'X-Proxy-Prefix' not in self.request.headers:
            return self.parent.finish_with_error(400)

        assert(self.request_uri(prefixize=False, with_query=False) == '/tests/controller/methods/request_uri/prefix')
        assert(self.request_uri(with_query=False) == '/controller/methods/request_uri/prefix')
        assert(self.prefixize(
            '/tests/controller/methods/request_uri/prefix') == '/controller/methods/request_uri/prefix')

        self.finish('done')
