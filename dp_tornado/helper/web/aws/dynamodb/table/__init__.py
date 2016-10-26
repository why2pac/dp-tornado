# -*- coding: utf-8 -*-


import time

from dp_tornado.engine.helper import Helper as dpHelper


class TableHelper(dpHelper):
    def get(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            wait_until_exists=False):
        dynamodb = self.helper.web.aws.dynamodb.resource(
            access_key_id=access_key_id, secret_access_key=secret_access_key, region_name=region_name)

        table = dynamodb.Table(table_name)

        if wait_until_exists:
            if not self.wait_until(
                    access_key_id=access_key_id,
                    secret_access_key=secret_access_key,
                    region_name=region_name,
                    table_name=table_name,
                    exists=True):
                return False

        return table

    def create(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            index_columns,
            read_capacity_units=1,
            write_capacity_units=1,
            wait_until_exists=True,
            **kwargs):
        try:
            dynamodb = self.helper.web.aws.dynamodb.client(
                access_key_id=access_key_id, secret_access_key=secret_access_key, region_name=region_name)

            def_at = self.helper.web.aws.dynamodb.table.indexing.sort

            key_schema = [{'AttributeName': e[0], 'KeyType': e[2] if len(e) >= 3 else def_at} for e in index_columns]
            attr_defs = [{'AttributeName': e[0], 'AttributeType': e[1]} for e in index_columns]

            dynamodb.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attr_defs,
                ProvisionedThroughput={
                    'ReadCapacityUnits': read_capacity_units,
                    'WriteCapacityUnits': write_capacity_units
                },
                **kwargs)

            if wait_until_exists:
                if not self.wait_until(
                        access_key_id=access_key_id,
                        secret_access_key=secret_access_key,
                        region_name=region_name,
                        table_name=table_name,
                        exists=True):
                    return False

            return True

        except Exception as e:
            if self.status(
                    access_key_id=access_key_id,
                    secret_access_key=secret_access_key,
                    region_name=region_name,
                    table_name=table_name) == 'ACTIVE':
                return True

            self.logging.exception(e)

            return False

    def wait_until(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            exists,
            repeat=25,
            repeated=0,
            before_status=None):
        try:
            status = self.status(
                access_key_id=access_key_id,
                secret_access_key=secret_access_key,
                region_name=region_name,
                table_name=table_name)

            if not status:
                if not exists and before_status in ('ACTIVE', 'DELETING'):
                    return True

                return False

            if exists and status == 'ACTIVE':
                return True

            if repeat > repeated:
                time.sleep(0.3)

                return self.wait_until(
                    access_key_id=access_key_id,
                    secret_access_key=secret_access_key,
                    region_name=region_name,
                    table_name=table_name,
                    exists=exists,
                    repeat=repeat,
                    repeated=repeated+1,
                    before_status=status)

            return True

        except Exception as e:
            self.logging.error(e)

            return False

    def status(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name):
        described = self.describe(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            region_name=region_name,
            table_name=table_name,
            wait_until_exists=False)

        if not described or 'Table' not in described or 'TableStatus' not in described['Table']:
            return False

        return described['Table']['TableStatus']

    def describe(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            wait_until_exists=True):
        try:
            if wait_until_exists:
                if not self.wait_until(
                        access_key_id=access_key_id,
                        secret_access_key=secret_access_key,
                        region_name=region_name,
                        table_name=table_name,
                        exists=True):
                    return False

            dynamodb = self.helper.web.aws.dynamodb.client(
                access_key_id=access_key_id, secret_access_key=secret_access_key, region_name=region_name)

            describe = dynamodb.describe_table(TableName=table_name)

            return describe

        except Exception as e:
            if wait_until_exists:
                self.logging.error(e)

            return False

    def remove(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            wait_until_not_exists=True):
        try:
            dynamodb = self.helper.web.aws.dynamodb.client(
                access_key_id=access_key_id, secret_access_key=secret_access_key, region_name=region_name)

            deleted = dynamodb.delete_table(TableName=table_name)

            if not deleted:
                return False

            if wait_until_not_exists:
                if not self.wait_until(
                        access_key_id=access_key_id,
                        secret_access_key=secret_access_key,
                        region_name=region_name,
                        table_name=table_name,
                        exists=False,
                        before_status='ACTIVE'):
                    return False

            return True

        except Exception as e:
            self.logging.exception(e)

            return False
