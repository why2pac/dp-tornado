# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class MysqlModel(dpModel):
    def index(self):
        self.model.tests.schema_test.migrate()

    @property
    def parent_test_id(self):
        return 100

    def test(self):
        datetime_of_birth = self.helper.datetime.now()

        self.execute_test_tuple(datetime_of_birth)
        assert self.scalar_test_tuple_name() == 'James'
        assert self.scalar_test_tuple_birth_year() == 1988

        dt_tuple_value = self.helper.datetime.tuple(datetime_of_birth)
        dt_tuple_fetch = self.helper.datetime.tuple(self.scalar_test_tuple_birth_datetime())

        assert dt_tuple_value == dt_tuple_fetch

        datetime_of_birth = self.helper.datetime.date.now()

        self.execute_test_dict(datetime_of_birth)
        assert self.scalar_test_dict() == 1989

        parent = self.row_test()

        dt_tuple_value = self.helper.datetime.tuple(datetime_of_birth)
        dt_tuple_fetch = self.helper.datetime.tuple(parent['datetime_of_birth'])

        assert dt_tuple_value == dt_tuple_fetch

        assert self.row_test()['parent_name'] == 'James'
        assert self.rows_test()[0]['parent_name'] == 'James'

        assert self.transaction_succ_test()
        assert not self.transaction_fail_test()

    def execute_test_tuple(self, datetime_of_birth):
        return self.execute("""
            INSERT INTO `parents`
                (`parent_id`, `parent_name`, `parent_type`, `year_of_birth`, `datetime_of_birth`)
                    VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            `parent_name` = VALUES(`parent_name`),
                            `parent_type` = VALUES(`parent_type`),
                            `year_of_birth` = VALUES(`year_of_birth`),
                            `datetime_of_birth` = VALUES(`datetime_of_birth`)
        """, (self.parent_test_id, 'James', 'FATHER', 1988, datetime_of_birth), 'tests.model_test/drv_mysql_test')

    def execute_test_dict(self, datetime_of_birth):
        params = {
            'parent_id': self.parent_test_id,
            'parent_name': 'James',
            'parent_type': 'FATHER',
            'year_of_birth': 1989,
            'datetime_of_birth': datetime_of_birth}

        return self.execute("""
            INSERT INTO `parents`
                (`parent_id`, `parent_name`, `parent_type`, `year_of_birth`, `datetime_of_birth`)
                    VALUES (%(parent_id)s, %(parent_name)s, %(parent_type)s, %(year_of_birth)s, %(datetime_of_birth)s)
                        ON DUPLICATE KEY UPDATE
                            `parent_name` = VALUES(`parent_name`),
                            `parent_type` = VALUES(`parent_type`),
                            `year_of_birth` = VALUES(`year_of_birth`),
                            `datetime_of_birth` = VALUES(`datetime_of_birth`)
        """, params, 'tests.model_test/drv_mysql_test')

    def scalar_test_tuple_name(self):
        return self.scalar("""
            SELECT
                `parent_name`
            FROM
                `parents`
            WHERE
                `parent_id` = %s
        """, self.parent_test_id, 'tests.model_test/drv_mysql_test')

    def scalar_test_tuple_birth_year(self):
        return self.scalar("""
            SELECT
                `year_of_birth`
            FROM
                `parents`
            WHERE
                `parent_id` = %s
        """, self.parent_test_id, 'tests.model_test/drv_mysql_test')

    def scalar_test_tuple_birth_datetime(self):
        return self.scalar("""
            SELECT
                `datetime_of_birth`
            FROM
                `parents`
            WHERE
                `parent_id` = %s
        """, self.parent_test_id, 'tests.model_test/drv_mysql_test')

    def scalar_test_dict(self):
        params = {
            'parent_id': self.parent_test_id,
            'parent_type': 'FATHER'
        }

        return self.scalar("""
            SELECT
                `year_of_birth`
            FROM
                `parents`
            WHERE
                `parent_id` = %(parent_id)s AND
                `parent_type` = %(parent_type)s
        """, params, 'tests.model_test/drv_mysql_test')

    def row_test(self):
        return self.row("""
            SELECT
                `parent_name`, `parent_type`, `year_of_birth`, `datetime_of_birth`
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
