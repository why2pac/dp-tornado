# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class DynamodbController(Controller):
    def get(self):
        for _ in range(3):
            try:
                table_name = 'dp_test_%s' % self.ini.server.identifier

                index_columns = [
                    ('key1', self.helper.web.aws.dynamodb.table.column.number, self.helper.web.aws.dynamodb.table.indexing.partition),
                    ('key2', self.helper.web.aws.dynamodb.table.column.string)
                ]

                created = self.helper.web.aws.dynamodb.table.create(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name,
                    index_columns=index_columns,
                    wait_until_exists=True)

                assert created

                described = self.helper.web.aws.dynamodb.table.describe(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name,
                    wait_until_exists=True)

                assert described and described['Table']['TableStatus'] == 'ACTIVE'

                items = (
                    {
                        'key1': 100,
                        'key2': 'a',
                        'ts': self.helper.datetime.timestamp.now(ms=True),
                        'identifier': self.ini.server.identifier
                    },
                    {
                        'key1': 110,
                        'key2': 'a',
                        'p1': 123,
                        'p2': 'abc',
                        'p3': None,
                        'p4': True,
                        'p5': False,
                        'p6': [1, 2],
                        'p7': ['한글', 123],
                        'p8': {
                            'a1': 123,
                            'a2': 'abc',
                            'a3': '한글',
                            'a4': [1, 2, 3],
                            'a5': ['abc', 123, 'def'],
                            'a6': True,
                            'a7': None
                        },
                        'ts': self.helper.datetime.timestamp.now(ms=True),
                        'identifier': self.ini.server.identifier
                    },
                    {
                        'key1': 120,
                        'key2': 'b',
                        'desc': 'will be deleted.',
                        'identifier': self.ini.server.identifier
                    }
                )

                inserted = self.helper.web.aws.dynamodb.item.put(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name,
                    items=items)

                assert inserted

                got = self.helper.web.aws.dynamodb.item.get(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name,
                    keys={'key1': 120, 'key2': 'b'})

                assert got['identifier'] == self.ini.server.identifier

                removed = self.helper.web.aws.dynamodb.item.remove(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name,
                    keys={'key1': 120, 'key2': 'b'})

                assert removed

                row = self.helper.web.aws.dynamodb.item.get(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name,
                    keys={'key1': 120, 'key2': 'b'})

                assert not row

                rows = self.helper.web.aws.dynamodb.item.get(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name,
                    keys=({'key1': 100, 'key2': 'a'}, {'key1': 110, 'key2': 'a'}))

                assert len(rows) == 2

                rows = self.helper.web.aws.dynamodb.item.query(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name,
                    ExpressionAttributeNames={
                        '#key1': 'key1'
                    },
                    ExpressionAttributeValues={
                        ':key1': 100
                    },
                    KeyConditionExpression='#key1 = :key1')

                assert len(rows) == 1

                count = self.helper.web.aws.dynamodb.item.query(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name,
                    count=True,
                    ExpressionAttributeNames={
                        '#key1': 'key1'
                    },
                    ExpressionAttributeValues={
                        ':key1': 100
                    },
                    KeyConditionExpression='#key1 = :key1')

                assert count == 1

                rows = self.helper.web.aws.dynamodb.item.scan(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name)

                assert len(rows) == 2

                count = self.helper.web.aws.dynamodb.item.scan(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name,
                    count=True)

                assert count == 2

                deleted = self.helper.web.aws.dynamodb.table.remove(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    table_name=table_name,
                    wait_until_not_exists=True)

                assert deleted

                return self.finish('done')

            except Exception as e:
                self.logging.exception(e)

        return self.finish_with_error(500)
