#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#

from engine.controller import Controller as dpController


class TestController(dpController):
    # URL matching with /foo/test
    def get(self):
        row = self.model.foo.bar.ex_row('youngyongpark@gmail.com')
        print(row)

        rows = self.model.foo.bar.ex_rows()
        print(rows)

        commit = self.model.foo.bar.ex_commit('youngyongpark@gmail.com')
        print(commit)

        rollback = self.model.foo.bar.ex_rollback('youngyongpark@gmail.com')
        print(rollback)

        row = self.model.foo.bar.ex_row('youngyongpark@gmail.com')
        print(row)

        self.finish('ok')