# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class GetArgumentController(Controller):
    def post(self):
        self.process()

    def get(self):
        self.process()

    def process(self):
        backup_zone = self.model.tests.helper_test.datetime.switch_timezone('Asia/Seoul')

        prepared = (
            ({'default': ' bar ', 'strip': False}, None, ' bar '),
            ({'default': ' bar ', 'strip': True}, None, ' bar '),
            ({'default': ' bar ', 'strip': False}, ' bar ', ' bar '),
            ({'default': ' bar ', 'strip': True}, ' bar ', 'bar'),

            ({'cast': object, 'fmt': 'yyyymmdd'}, '19890203', self.helper.datetime.convert(timestamp=602434800)),
            ({'cast': object, 'fmt': 'yyyymmdd'}, '1989-02-03', self.helper.datetime.convert(timestamp=602434800)),
            ({'cast': object, 'fmt': 'yyyymmdd'}, '1989/02/03', self.helper.datetime.convert(timestamp=602434800)),
            ({'cast': object, 'fmt': 'yyyymmddhhiiss'}, '19890203092030', self.helper.datetime.convert(timestamp=602468430)),
            ({'cast': object, 'fmt': 'yyyymmddhhiiss'}, '1989-02-03 09:20:30', self.helper.datetime.convert(timestamp=602468430)),
            ({'cast': object, 'fmt': 'yyyymmddhhiiss'}, '1989/02/03 09:20:30', self.helper.datetime.convert(timestamp=602468430)),
            ({'cast': object, 'fmt': 'yyyymmddhhiiss'}, '1989/02/03 092030', self.helper.datetime.convert(timestamp=602468430)),

            ({'cast': self.helper.misc.type.int, 'fmt': 'yyyymmdd'}, '19890203', 602434800),
            ({'cast': self.helper.misc.type.int, 'fmt': 'yyyymmdd'}, '1989-02-03', 602434800),
            ({'cast': self.helper.misc.type.int, 'fmt': 'yyyymmdd'}, '1989/02/03', 602434800),
            ({'cast': self.helper.misc.type.int, 'fmt': 'yyyymmddhhiiss'}, '19890203092030', 602468430),
            ({'cast': self.helper.misc.type.int, 'fmt': 'yyyymmddhhiiss'}, '1989-02-03 09:20:30', 602468430),
            ({'cast': self.helper.misc.type.int, 'fmt': 'yyyymmddhhiiss'}, '1989/02/03 09:20:30', 602468430),
            ({'cast': self.helper.misc.type.int, 'fmt': 'yyyymmddhhiiss'}, '1989/02/03 092030', 602468430),

            ({'cast': self.helper.misc.type.long, 'fmt': 'yyyymmdd'}, '19890203', 602434800),
            ({'cast': self.helper.misc.type.long, 'fmt': 'yyyymmdd'}, '1989-02-03', 602434800),
            ({'cast': self.helper.misc.type.long, 'fmt': 'yyyymmdd'}, '1989/02/03', 602434800),
            ({'cast': self.helper.misc.type.long, 'fmt': 'yyyymmddhhiiss'}, '19890203092030', 602468430),
            ({'cast': self.helper.misc.type.long, 'fmt': 'yyyymmddhhiiss'}, '1989-02-03 09:20:30', 602468430),
            ({'cast': self.helper.misc.type.long, 'fmt': 'yyyymmddhhiiss'}, '1989/02/03 09:20:30', 602468430),
            ({'cast': self.helper.misc.type.long, 'fmt': 'yyyymmddhhiiss'}, '1989/02/03 092030', 602468430),

            ({'cast': self.helper.misc.type.float, 'fmt': 'yyyymmdd'}, '19890203', 602434800),
            ({'cast': self.helper.misc.type.float, 'fmt': 'yyyymmdd'}, '1989-02-03', 602434800),
            ({'cast': self.helper.misc.type.float, 'fmt': 'yyyymmdd'}, '1989/02/03', 602434800),
            ({'cast': self.helper.misc.type.float, 'fmt': 'yyyymmddhhiiss'}, '19890203092030', 602468430),
            ({'cast': self.helper.misc.type.float, 'fmt': 'yyyymmddhhiiss'}, '1989-02-03 09:20:30', 602468430),
            ({'cast': self.helper.misc.type.float, 'fmt': 'yyyymmddhhiiss'}, '1989/02/03 09:20:30', 602468430),
            ({'cast': self.helper.misc.type.float, 'fmt': 'yyyymmddhhiiss'}, '1989/02/03 092030', 602468430),

            ({'cast': 'numeric'}, '123,456aa', '123456'),
            ({'cast': self.helper.misc.type.int, 'fmt': 'numeric'}, '123,456aa', 123456),
            ({'cast': self.helper.misc.type.long, 'fmt': 'numeric'}, '123,456aa', 123456),
            ({'cast': self.helper.misc.type.float, 'fmt': 'numeric'}, '123,456aa', 123456.0),

            ({'cast': self.helper.misc.type.int}, '123,456', False),
            ({'cast': self.helper.misc.type.int}, '123456', 123456),
            ({'cast': self.helper.misc.type.int}, '123456.7', False),
            ({'cast': self.helper.misc.type.long}, '123,456', False),
            ({'cast': self.helper.misc.type.long}, '123456', 123456),
            ({'cast': self.helper.misc.type.long}, '123456.7', False),
            ({'cast': self.helper.misc.type.float}, '123,456', False),
            ({'cast': self.helper.misc.type.float}, '123456', 123456),
            ({'cast': self.helper.misc.type.float}, '123456.7', 123456.7),

            ({'cast': self.helper.misc.type.bool}, '1', True),
            ({'cast': self.helper.misc.type.bool}, 'y', True),
            ({'cast': self.helper.misc.type.bool}, 'Y', True),
            ({'cast': self.helper.misc.type.bool}, 'T', True),
            ({'cast': self.helper.misc.type.bool}, 't', True),
            ({'cast': self.helper.misc.type.bool}, 'YES', True),
            ({'cast': self.helper.misc.type.bool}, 'Yes', True),
            ({'cast': self.helper.misc.type.bool}, 'yes', True),
            ({'cast': self.helper.misc.type.bool}, 'TRUE', True),
            ({'cast': self.helper.misc.type.bool}, 'True', True),
            ({'cast': self.helper.misc.type.bool}, 'true', True),
            ({'cast': self.helper.misc.type.bool}, '0', False),
            ({'cast': self.helper.misc.type.bool}, 'N', False),
            ({'cast': self.helper.misc.type.bool}, 'F', False),
            ({'cast': self.helper.misc.type.bool}, 'NO', False),
            ({'cast': self.helper.misc.type.bool}, 'FALSE', False),
            ({'cast': self.helper.misc.type.bool}, 'OK', -1),

            ({'fmt': 'json'}, 'dummy', False),
            ({'cast': 'json'}, 'dummy', False),

            ({'fmt': 'json'}, self.helper.string.serialization.serialize({'foo': 'bar'}), {'foo': 'bar'}),
            ({'cast': 'json'}, self.helper.string.serialization.serialize({'foo': 'bar'}), {'foo': 'bar'}),

            ({'delimiter': ','}, '1,2,3', ('1', '2', '3')),

            ({'fmt': 'url'}, 'xxx://www.google.com', False),
            ({'fmt': 'url'}, 'http://www.google.com', 'http://www.google.com'),

            ({'fmt': 'email'}, 'user@@domain.com', False),
            ({'fmt': 'email'}, 'user@domain.com', 'user@domain.com'),

            ({'fmt': 'email-username'}, 'user@', False),
            ({'fmt': 'email-username'}, 'user', 'user'),

            ({'fmt': 'email-domain'}, '@domain', False),
            ({'fmt': 'email-domain'}, 'domain.com', 'domain.com'),

            ({'fmt': 'html'}, '<a href="javascript:void(0);">tag', '<a href="javascript:void(0);">tag</a>'),
            ({'fmt': 'xss'}, '<a href="javascript:void(0);">tag', 'tag'),
        )

        if self.get_argument('mode') != 'test':
            url = self.request_uri(with_query=False)
            queries = {'mode': 'test'}

            offset = 0
            for e in prepared:
                offset += 1

                if e[1]:
                    queries['val_%s' % offset] = e[1]

            url = self.helper.web.url.parse(url)
            url.scheme = self.request.protocol
            url.netloc = self.request.host

            status_code, response = self.helper.web.http.post.text(self.helper.web.url.build(url), data=queries)

            self.model.tests.helper_test.datetime.set_timezone(backup_zone)

            assert status_code == 200
            return self.finish(response)

        offset = 0
        for e in prepared:
            offset += 1

            val = self.get_argument('val_%s' % offset, **e[0])
            exp = e[2]

            if isinstance(val, (list, tuple)):
                val = str([str(e) for e in val])
                exp = str([str(e) for e in exp])

            print(val == exp, '[%s]' % exp, '[%s]' % val, type(val))
            assert val == exp

        self.model.tests.helper_test.datetime.set_timezone(backup_zone)

        self.finish('done')
