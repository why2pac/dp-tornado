# -*- coding: utf-8 -*-


import time

from dp_tornado.engine.controller import Controller


class TestController(Controller):
    # URL matching with /foo/test
    def get(self):
        session = self.session('val')
        print(session)

        self.session('val', 'assigned!!!')
        session = self.session('val')
        print(session)

        self.model.foo.bar.create()
        print('table created')

        uuid = self.helper.random.uuid()

        self.model.foo.bar.insert(uuid)
        print('inserted')

        row = self.model.foo.bar.ex_row(uuid)
        print(row)

        time.sleep(1.5)

        rows = self.model.foo.bar.ex_rows()
        print(rows)

        commit = self.model.foo.bar.ex_commit(uuid)
        print(commit)

        time.sleep(1.5)

        rollback = self.model.foo.bar.ex_rollback(uuid)
        print(rollback)

        time.sleep(1.5)

        row = self.model.foo.bar.ex_row(uuid)
        print(row)

        time.sleep(1.5)

        test = self.model.foo.bar.ex_local()
        print(test)

        self.finish('ok')
