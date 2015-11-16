# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class BarModel(dpModel):
    def create(self):
        return self.execute("""
            CREATE TABLE IF NOT EXISTS userinfo (
                user_id TEXT PRIMARY KEY ASC NOT NULL,
                updatedate INT DEFAULT NULL
            )
        """, None, 'foo.bar/bar')

    def insert(self, user_id):
        return self.execute("""
            INSERT INTO userinfo
                (user_id, updatedate) VALUES (?, ?)
        """, (user_id, self.helper.datetime.time()), 'foo.bar/bar')

    # Method callable by self.model.foo.bar.user.ex_row from Controller
    def ex_row(self, user_id):
        return self.row("""
            SELECT * FROM userinfo WHERE user_id = ?
        """, user_id, 'foo.bar/bar')

    # Method callable by self.model.foo.bar.user.ex_rows from Controller
    def ex_rows(self):
        return self.rows("""
            SELECT * FROM userinfo LIMIT 10
        """, None, 'foo.bar/bar')

    # Method callable by self.model.foo.bar.user.ex_commit from Controller
    def ex_commit(self, user_id):
        proxy = self.begin('foo.bar/bar')

        before = proxy.row("""
            SELECT * FROM userinfo WHERE user_id = ?
        """, user_id)

        print('before : %s' % before)

        proxy.execute("""
            UPDATE userinfo SET updatedate = ? WHERE user_id = ?
        """, (self.helper.datetime.time(), user_id))

        after = proxy.row("""
            SELECT * FROM userinfo WHERE user_id = ?
        """, user_id)

        print('after : %s' % after)

        proxy.commit(proxy)

    # Method callable by self.model.foo.bar.user.ex_rollback from Controller
    def ex_rollback(self, user_id):
        proxy = self.begin('foo.bar/bar')

        before = proxy.row("""
            SELECT * FROM userinfo WHERE user_id = ?
        """, user_id)

        print('before : %s' % before)

        proxy.execute("""
            UPDATE userinfo SET updatedate = ? WHERE user_id = ?
        """, (self.helper.datetime.time(), user_id))

        after = proxy.row("""
            SELECT * FROM userinfo WHERE user_id = ?
        """, user_id)

        print('after : %s' % after)

        proxy.rollback(proxy)

    def ex_local(self):
        return self.execute("""
            CREATE TABLE IF NOT EXISTS a (b INT, c TEXT)
        """, None, 'foo.bar/local')
