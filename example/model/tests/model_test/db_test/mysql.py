# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class MysqlModel(dpModel):
    def index(self):
        self.model.tests.schema_test.migrate()

    @property
    def parent_test_id(self):
        return 100

    def test(self):
        assert self.execute_test().rowcount == 1
        assert self.scalar_test() == 'James'
        assert self.row_test()['parent_name'] == 'James'
        assert self.rows_test()[0]['parent_name'] == 'James'
        assert self.transaction_succ_test()
        assert not self.transaction_fail_test()

    def execute_test(self):
        return self.execute("""
            INSERT INTO `parents`
                (`parent_id`, `parent_name`, `parent_type`)
                    VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            `parent_name` = VALUES(`parent_name`),
                            `parent_type` = VALUES(`parent_type`)
        """, (self.parent_test_id, 'James', 'FATHER'), 'tests.model_test/drv_mysql_test')

    def scalar_test(self):
        return self.scalar("""
            SELECT
                `parent_name`
            FROM
                `parents`
            WHERE
                `parent_id` = %s
        """, self.parent_test_id, 'tests.model_test/drv_mysql_test')

    def row_test(self):
        return self.row("""
            SELECT
                `parent_name`, `parent_type`
            FROM
                `parents`
            WHERE
                `parent_id` = %s
        """, self.parent_test_id, 'tests.model_test/drv_mysql_test')

    def rows_test(self):
        return self.rows("""
            SELECT
                `parent_name`, `parent_type`
            FROM
                `parents`
            WHERE
                `parent_id` = %s
        """, self.parent_test_id, 'tests.model_test/drv_mysql_test')

    def transaction_succ_test(self):
        tran = self.begin('tests.model_test/drv_mysql_test')

        try:
            tran.execute("""
                INSERT INTO `parents`
                    (`parent_id`, `parent_name`, `parent_type`)
                        VALUES (%s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                                `parent_name` = VALUES(`parent_name`),
                                `parent_type` = VALUES(`parent_type`)
            """, (self.parent_test_id + 1, 'James', 'FATHER'))

            tran.commit()

            return True

        except Exception as e:
            tran.rollback()

            return False

    def transaction_fail_test(self):
        tran = self.begin('tests.model_test/drv_mysql_test')

        try:
            tran.execute("""
                INSERT INTO `childs`
                    (`parent_id`, `child_name`, `child_type`)
                        VALUES (%s, %s, %s)
            """, (self.parent_test_id + 9999, 'Kim', 'MOTHER'))

            tran.commit()

            return True

        except Exception as e:
            tran.rollback()

            return False
