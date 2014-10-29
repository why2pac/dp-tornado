#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from engine.model import Model as dpModel


class BarModel(dpModel):
    # Method callable by self.model.foo.bar.user.ex_row from Controller
    def ex_row(self, user_id):
        return self.row(
            'SELECT * FROM userinfo WHERE user_id = %s', user_id, 'foo.bar/bar')

    # Method callable by self.model.foo.bar.user.ex_rows from Controller
    def ex_rows(self):
        return self.rows(
            'SELECT * FROM userinfo LIMIT 10', None, 'foobar/bar')

    # Method callable by self.model.foo.bar.user.ex_commit from Controller
    def ex_commit(self, user_id):
        proxy = self.begin('foo.bar/bar')

        before = proxy.row('SELECT * FROM userinfo WHERE user_id = %s', user_id)
        print('before : %s' % before)

        proxy.execute('UPDATE userinfo SET registered_date=33, lately_login_date=66 WHERE user_id=%s', user_id)

        after = proxy.row('SELECT * FROM userinfo WHERE user_id = %s', user_id)
        print('after : %s' % after)

        proxy.commit(proxy)

    # Method callable by self.model.foo.bar.user.ex_rollback from Controller
    def ex_rollback(self, user_id):
        proxy = self.begin('foobar/bar')

        before = proxy.row('SELECT * FROM userinfo WHERE user_id = %s', user_id, proxy)
        print('before : %s' % before)

        proxy.execute('UPDATE userinfo SET registered_date=33, lately_login_date=44 WHERE user_id=%s', user_id, proxy)

        after = proxy.row('SELECT * FROM userinfo WHERE user_id = %s', user_id, proxy)
        print('after : %s' % after)

        proxy.rollback(proxy)