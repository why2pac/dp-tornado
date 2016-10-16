# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class UuidController(Controller):
    def get(self):
        assert(len(str(self.helper.misc.uuid.namespace_dns)) == 36)
        assert(len(str(self.helper.misc.uuid.namespace_url)) == 36)
        assert(len(str(self.helper.misc.uuid.namespace_oid)) == 36)
        assert(len(str(self.helper.misc.uuid.namespace_x500)) == 36)
        assert(len(self.helper.misc.uuid.v1()) == 36)
        assert(len(self.helper.misc.uuid.v3(self.helper.misc.uuid.namespace_dns, 'test.com')) == 36)
        assert(len(self.helper.misc.uuid.v4()) == 36)
        assert(len(self.helper.misc.uuid.v5(self.helper.misc.uuid.namespace_dns, 'test.com')) == 36)
