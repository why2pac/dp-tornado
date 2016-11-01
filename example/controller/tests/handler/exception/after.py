# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class AfterController(Controller):
    def get(self):
        payload = self.model.tests.handler.exception.get()
        payload = self.helper.string.serialization.deserialize(payload)

        assert payload
        assert 'dummy_value' in payload['msg']

        self.finish('done')
