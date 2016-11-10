# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class TestController(Controller):
    def get(self):
        uuid_key = self.helper.misc.uuid.v1()
        uuid_val = self.helper.misc.uuid.v1()

        host = '%s://%s' % (self.request.protocol, self.request.host)
        url_get = '%s/tests/controller/session/get/%s' % (host, uuid_key)
        url_set = '%s/tests/controller/session/set/%s/%s' % (host, uuid_key, uuid_val)

        sess, code, res = self.helper.web.http.request('get', 'text', url_get, session=True)

        assert sess and code == 200 and res == 'empty'

        sess_set, code, res = self.helper.web.http.request('get', 'text', url_set, session=True)

        assert sess and code == 200 and res == 'done'

        sess, code, res = self.helper.web.http.request('get', 'text', url_get, session=True)

        assert sess and code == 200 and res == 'empty'

        sess, code, res = self.helper.web.http.request('get', 'text', url_get, session=sess_set)

        assert sess and code == 200 and res == uuid_val

        self.finish('done')
