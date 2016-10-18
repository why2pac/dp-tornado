# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller
from bs4 import BeautifulSoup


class PrefixController(Controller):
    def get(self):
        params = {
            'total_count': 100,
            'page': 3,
            'rpp': 10,
            'kwargs': {

            }
        }

        pagination = self.render_string('tests/view/module/pagination.html', params)
        pagination = BeautifulSoup(pagination, 'lxml')

        request_uri = self.request_uri(with_query=False)

        assert(request_uri == '/view/module/pagination/prefix')

        for e in pagination.findAll('a'):
            assert(str(e.attrs['href']).startswith(request_uri) is True)

        self.finish('done')
