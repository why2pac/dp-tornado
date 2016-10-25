# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class DynamodbController(Controller):
    def get(self):
        table_name = 'dp_test_%s' % self.ini.server.identifier

        index_columns = [
            ('key1', self.helper.web.aws.dynamodb.column.number, self.helper.web.aws.dynamodb.indexing.partition),
            ('key2', self.helper.web.aws.dynamodb.column.string)
        ]

        created = self.helper.web.aws.dynamodb.create_table(
            access_key_id=self.ini.static.aws_id,
            secret_access_key=self.ini.static.aws_secret,
            region_name=self.ini.static.aws_region,
            table_name=table_name,
            index_columns=index_columns,
            wait_until_exists=True)

        assert created

        described = self.helper.web.aws.dynamodb.describe_table(
            access_key_id=self.ini.static.aws_id,
            secret_access_key=self.ini.static.aws_secret,
            region_name=self.ini.static.aws_region,
            table_name=table_name,
            wait_until_exists=True)

        assert described

        deleted = self.helper.web.aws.dynamodb.remove_table(
            access_key_id=self.ini.static.aws_id,
            secret_access_key=self.ini.static.aws_secret,
            region_name=self.ini.static.aws_region,
            table_name=table_name,
            wait_until_not_exists=True)

        assert deleted

        self.finish('done')
