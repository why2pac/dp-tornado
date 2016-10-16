# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class SessionIdController(Controller):
    def get(self):
        sessionid = self.get_sessionid()
        hashed = self.helper.security.crypto.hash.sha224('test')

        assert(len(sessionid) == len(hashed))

        self.finish('done')
