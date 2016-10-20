# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class FormController(Controller):
    def post(self):
        self.process()

    def get(self):
        self.process()

    def process(self):
        backup_zone = self.model.tests.helper_test.datetime.switch_timezone('Asia/Seoul')

        testset = (
            (
                (
                    ({'cast': object, 'fmt': 'yyyymmdd'}, '19890203'),
                    ({'cast': object, 'fmt': 'yyyymmddhhiiss'}, '19890203092030'),

                    ({'cast': self.helper.misc.type.int, 'fmt': 'yyyymmdd'}, '19890203'),
                    ({'cast': self.helper.misc.type.int, 'fmt': 'yyyymmddhhiiss'}, '19890203092030'),

                    ({'cast': 'numeric'}, '123,456aa', '123456'),
                    ({'cast': self.helper.misc.type.int, 'fmt': 'numeric'}, '123,456aa'),
                    ({'cast': self.helper.misc.type.long, 'fmt': 'numeric'}, '123,456aa'),
                    ({'cast': self.helper.misc.type.float, 'fmt': 'numeric'}, '123,456aa'),

                    ({'cast': self.helper.misc.type.int}, '123456'),
                    ({'cast': self.helper.misc.type.long}, '123456'),
                    ({'cast': self.helper.misc.type.float}, '123456.7'),

                    ({'cast': self.helper.misc.type.bool}, 'Y'),
                    ({'cast': self.helper.misc.type.bool}, 'F'),

                    ({'fmt': 'json'}, self.helper.string.serialization.serialize({'foo': 'bar'})),
                    ({'cast': 'json'}, self.helper.string.serialization.serialize({'foo': 'bar'})),

                    ({'delimiter': ','}, '1,2,3'),

                    ({'fmt': 'url'}, 'http://www.google.com'),
                    ({'fmt': 'html'}, '<a href="javascript:void(0);">tag'),
                    ({'fmt': 'xss'}, '<a href="javascript:void(0);">tag')
                ),
                {
                    'result': True
                }
            ),
            (
                (
                    ({'cast': self.helper.misc.type.bool, 'invalid': 'invalid bool value'}, 'OK'),
                ),
                {
                    'result': False,
                    'error': {
                        'field': 'val_1',
                        'reason': 'invalid',
                        'message': 'invalid bool value'
                    }
                }
            ),
            (
                (
                    ({'cast': self.helper.misc.type.bool, 'required': True, 'missing': 'missing bool value'}, None),
                ),
                {
                    'result': False,
                    'error': {
                        'field': 'val_1',
                        'reason': 'missing',
                        'message': 'missing bool value'
                    }
                }
            )
        )

        if self.get_argument('mode') != 'test':
            url = self.request_uri(with_query=False)
            url = self.helper.web.url.parse(url)
            url.scheme = self.request.protocol
            url.netloc = self.request.host

            p_offset = 0
            for ee in testset:
                prepared = ee[0]
                p_offset += 1
                queries = {'mode': 'test', 'offset': p_offset}

                offset = 0
                for e in prepared:
                    offset += 1

                    if e[1]:
                        queries['val_%s' % offset] = e[1]

                status_code, res = self.helper.web.http.post.json(self.helper.web.url.build(url), data=queries)
                exp = (self.helper.string.serialization.deserialize(self.helper.string.serialization.serialize(ee[1])))

                assert res == exp

            self.model.tests.helper_test.datetime.set_timezone(backup_zone)

            return self.finish('done')

        p_offset = self.get_argument('offset', cast=int)

        form = {}

        prepared = testset[p_offset-1]

        offset = 0
        for e in prepared[0]:
            offset += 1
            form['val_%s' % offset] = e[0]

        validate = self.helper.validator.form.validate(self, form)

        self.model.tests.helper_test.datetime.set_timezone(backup_zone)

        if not validate:
            return False

        self.finish({'result': True})
