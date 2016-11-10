# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class SessionController(Controller):
    def get(self):
        """
            .. test::
                expect(2, code=200, text='done')
        """

        if self.session(self.ini.server.identifier) == 'assigned':
            return self.finish('done')

        self.finish_with_error(400)

    def post(self):
        """
            .. test::
                expect(1, code=200)
        """

        self.session(self.ini.server.identifier, 'assigned')

        self.finish('done')
