# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class SchemaTestModel(dpModel):
    def index(self):
        self.execute("""DROP DATABASE IF EXISTS `dp_test`""", None, 'tests.model_test/drv_mysql_sys')
        self.execute("""CREATE DATABASE IF NOT EXISTS `dp_test`""", None, 'tests.model_test/drv_mysql_sys')

    def migrate(self):
        if getattr(self, '__tested__', None):
            return True

        self.migrate_unittest()
        self.migrate_migration()

        setattr(self, '__tested__', True)

    def migrate_unittest(self):
        self.schema.tests.unittest.toys.migrate()
        self.schema.tests.unittest.parents.migrate()
        self.schema.tests.unittest.childs.migrate()
        self.schema.tests.unittest.child_toys.migrate()

        self.migrate_unittest_toys_assert()
        self.migrate_unittest_child_toys_assert()

        self.migrate_unittest_data_assert()

    def migrate_unittest_toys_assert(self):
        offset = 0

        fields = (
            ('toy_id', 'bigint(20) unsigned', 'no', 'pri', '', 'auto_increment'),
            ('toy_code', 'bigint(20) unsigned zerofill', 'no', '', '', ''),
            ('toy_name', "varchar(128)", 'no', 'mul', '', ''),
            ('toy_summary', 'text', 'no', 'mul', '', ''),
            ('toy_description', 'longtext', 'no', 'mul', '', '')
        )

        for e in self.rows("""
            SHOW COLUMNS FROM %s
                """ % self.schema.tests.unittest.toys.__table_name__, None, 'tests.model_test/drv_mysql_test'):
            assert ((e[0] or '').lower() == fields[offset][0] and
                    (e[1] or '').lower() == fields[offset][1] and
                    (e[2] or '').lower() == fields[offset][2] and
                    (e[3] or '').lower() == fields[offset][3] and
                    (e[4] or '').lower() == fields[offset][4] and
                    (e[5] or '').lower() == fields[offset][5])

            offset += 1

    def migrate_unittest_child_toys_assert(self):
        offset = 0

        fields = (
            ('child_id', 'bigint(20) unsigned', 'NO', 'PRI', None, ''),
            ('toy_id', 'bigint(20) unsigned', 'NO', 'PRI', None, '')
        )

        for e in self.rows("""
            SHOW COLUMNS FROM %s
                """ % self.schema.tests.unittest.child_toys.__table_name__, None, 'tests.model_test/drv_mysql_test'):
            assert self._assert_fields(e, fields[offset])

            offset += 1

        offset = 0

        fields = (
            ('child_toys', 0, 'PRIMARY', 1, 'child_id', 'A', 0, None, None, '', 'BTREE', '', ''),
            ('child_toys', 0, 'PRIMARY', 2, 'toy_id', 'A', 0, None, None, '', 'BTREE', '', ''),
            ('child_toys', 0, 'uk_child_toys_toy_id', 1, 'toy_id', 'A', 0, None, None, '', 'BTREE', '', '')
        )

        for e in self.rows("""
            SHOW INDEX FROM %s
                """ % self.schema.tests.unittest.child_toys.__table_name__, None, 'tests.model_test/drv_mysql_test'):
            assert self._assert_fields(e, fields[offset])

            offset += 1

    def migrate_unittest_data_assert(self):
        # Insert Parents

        parent_park_id = 1

        self.execute("""
            INSERT INTO `parents`
                (`parent_id`, `parent_name`, `parent_type`)
                    VALUES (%s, %s, %s)
        """, (parent_park_id, 'Park', 'FATHER'), 'tests.model_test/drv_mysql_test')

        tran = self.begin('tests.model_test/drv_mysql_test')

        try:
            tran.execute("""
                INSERT INTO `parents`
                    (`parent_name`, `parent_type`)
                        VALUES (%s, %s)
            """, ('Kim', 'MOTHER'))

            parent_kim_id = tran.scalar('SELECT last_insert_id()')

            assert parent_kim_id and parent_kim_id > parent_park_id

            tran.commit()

        except Exception as e:
            tran.rollback()

            raise e

        # Insert Childs

        self.execute("""
            INSERT INTO `childs`
                (`parent_id`, `child_name`, `child_type`)
                    VALUES (%s, %s, %s)
        """, (parent_park_id, 'Lee', 'GIRL'), 'tests.model_test/drv_mysql_test')

        try:
            tran.execute("""
                INSERT INTO `childs`
                    (`parent_id`, `child_name`, `child_type`)
                        VALUES (%s, %s, %s)
            """, (9999999, 'Kim', 'MOTHER'))

            parent_kim_id = tran.scalar('SELECT last_insert_id()')

            # SHOULD NOT REACH HERE.

            assert not parent_kim_id

            tran.commit()

        except Exception as e:
            tran.rollback()

            # SHOULD REACH HERE, parent_id:9999999 is not exists. Violates foreign key constraint.

            assert True

    def migrate_migration(self):
        self.schema.tests.migration.first.migrate()
        self.migrate_migration_first_assert()

        self.schema.tests.migration.second.migrate()
        self.migrate_migration_second_assert()

    def migrate_migration_first_assert(self):
        offset = 0

        fields = (
            ('migration_id', 'bigint(20) unsigned', 'NO', 'PRI', None, 'auto_increment'),
            ('migration_name', 'char(128)', 'NO', '', None, ''),
            ('migration_type', "enum('AUTO','MANUAL')", 'NO', '', 'AUTO', ''),
            ('signdate', 'int(11)', 'NO', '', None, '')
        )

        for e in self.rows("""
            SHOW COLUMNS FROM %s
                """ % self.schema.tests.migration.first.__table_name__, None, 'tests.model_test/drv_mysql_test'):
            assert self._assert_fields(e, fields[offset])

            offset += 1

    def migrate_migration_second_assert(self):
        offset = 0

        fields = (
            ('migration_id', 'bigint(20) unsigned', 'NO', 'PRI', None, 'auto_increment'),
            ('migration_name', 'varchar(128)', 'NO', '', None, ''),
            ('migration_type', "enum('AUTO','MANUAL','NONE')", 'NO', '', 'NONE', ''),
            ('updatedate', 'int(11)', 'NO', '', None, '')
        )

        for e in self.rows("""
            SHOW COLUMNS FROM %s
                """ % self.schema.tests.migration.second.__table_name__, None, 'tests.model_test/drv_mysql_test'):
            assert self._assert_fields(e, fields[offset])

            offset += 1

    def _assert_fields(self, a, b):
        str_type = type('')

        if len(a) != len(b):
            return False

        for i in range(len(a)):
            if isinstance(b[i], str_type):
                if ('%s' % (a[i] or '')).lower() != ('%s' % (b[i] or '')).lower():
                    return False
            elif a[i] != b[i]:
                return False

        return True
