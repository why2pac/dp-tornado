# -*- coding: utf-8 -*-


import time
import tornado.httpclient

from dp_tornado.engine.controller import Controller


class RunAloneController(Controller):
    def get(self):
        cb = {
            'succ': 0,
            'fail': 0
        }

        self._request('tests/model/cache/decorator/run_alone/test', 'done', cb)
        self._request('tests/model/cache/decorator/run_alone/test', 'busy', cb)

        for e in range(10):
            time.sleep(1)

            if cb['succ'] + cb['fail'] == 2:
                break

        print(cb)

        assert cb['fail'] == 0 and cb['succ'] == 2

        cb['succ'] = 0
        cb['fail'] = 0

        self._request('tests/model/cache/decorator/run_alone/test_with_exp', 'done', cb)
        self._request('tests/model/cache/decorator/run_alone/test_with_exp', 'busy', cb)

        time.sleep(3)
        self._request('tests/model/cache/decorator/run_alone/test_with_exp', 'done', cb)

        for e in range(10):
            time.sleep(1)

            if cb['succ'] + cb['fail'] == 3:
                break

        print(cb)

        assert cb['fail'] == 0 and cb['succ'] == 3

        self.finish('done')

    def _request(self, url, exp, cb):
        def handle_response(res):
            res = res.body

            if self.helper.misc.system.py_version >= 3:
                res = res.decode('utf8')

            print(url, exp, res)

            if self.helper.string.cast.string(res) == exp:
                cb['succ'] += 1
            else:
                cb['fail'] += 1

        try:
            url = '%s://%s/%s' % (self.request.protocol, self.request.host, url)

            http_client = tornado.httpclient.AsyncHTTPClient()
            http_client.fetch(url, handle_response)

        except Exception as e:
            cb['fail'] += 1

            self.logging.exception(e)

