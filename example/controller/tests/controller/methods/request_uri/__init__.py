# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class RequestUriController(Controller):
    def get(self):
        if not self.get_argument('foo'):
            uri = self.request_uri(with_query=False)
            uri = self.helper.web.url.build(uri, {'foo': 'bar'})

            return self.redirect(uri)

        uri = self.request_uri()
        uri_without_query = self.request_uri(with_query=False)
        uri_prefixize = self.request_uri(prefixize=False)
        uri_encoded = self.request_uri(urlencode=True)
        uri_encoded_decode = self.helper.web.url.decode(uri_encoded)

        assert(uri == '/tests/controller/methods/request_uri?foo=bar')
        assert(uri_without_query == '/tests/controller/methods/request_uri')
        assert(uri_prefixize == '/tests/controller/methods/request_uri?foo=bar')
        assert(uri_encoded == '%2Ftests%2Fcontroller%2Fmethods%2Frequest_uri%3Ffoo%3Dbar')
        assert(uri_encoded_decode == uri_prefixize)
