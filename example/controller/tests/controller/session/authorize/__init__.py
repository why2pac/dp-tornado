# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class AuthorizeController(Controller):
    def get(self):
        """

            .. test::
                expect(10, code=200, text='unauthorized')

                expect(21, code=200, text='testuser')
                expect(23, code=200, text='unauthorized')
        """
        authorized = self.helper.misc.session.authorized(self, 'appname')

        if not authorized:
            return self.finish('unauthorized')

        self.finish(authorized['userid'])

    def post(self):
        """

            .. test::
                expect(10, code=400)

                expect(20, code=200, text='authorized', params={'userid': 'testuser', 'password': 'password'})
        """
        userid = self.get_argument('userid')
        password = self.get_argument('password')

        if not userid or not password:
            return self.finish_with_error(400)

        if not self.helper.misc.session.authorize(self, 'appname', {'userid': userid}, after=self._after_authorize):
            return self.finish_with_error(500)

        assert getattr(self, '_after_authorize_executed') == 'yes'

        if not self.helper.misc.session.is_authorized(self, 'appname'):
            return self.finish_with_error(500)

        self.finish('authorized')

    def _after_authorize(self, payload):
        setattr(self, '_after_authorize_executed', 'yes')

    def delete(self):
        """

            .. test::
                expect(22, code=200, text='unauthorized')
        """
        if not self.helper.misc.session.unauthorize(self, 'appname'):
            return self.finish_with_error(500)

        self.finish('unauthorized')
