# -*- coding: utf-8 -*-


import time
import boto3

from dp_tornado.engine.helper import Helper as dpHelper


class DynamodbHelper(dpHelper):
    def create_table(
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
            dynamodb = boto3.client(
                service_name='dynamodb',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name)

            def_at = self.helper.web.aws.dynamodb.indexing.sort

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
                if not self.wait_until_table(
                        access_key_id=access_key_id,
                        secret_access_key=secret_access_key,
                        region_name=region_name,
                        table_name=table_name,
                        exists=True):
                    return False

            return True

        except Exception as e:
            self.logging.exception(e)

            return False

    def wait_until_table(
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
            described = self.describe_table(
                access_key_id=access_key_id,
                secret_access_key=secret_access_key,
                region_name=region_name,
                table_name=table_name,
                wait_until_exists=False)

            if not described:
                if not exists and before_status in ('ACTIVE', 'DELETING'):
                    return True

                return False

            if exists and described['Table']['TableStatus'] == 'ACTIVE':
                return True

            if repeat > repeated:
                time.sleep(0.3)

                return self.wait_until_table(
                    access_key_id=access_key_id,
                    secret_access_key=secret_access_key,
                    region_name=region_name,
                    table_name=table_name,
                    exists=exists,
                    repeat=repeat,
                    repeated=repeated+1,
                    before_status=described['Table']['TableStatus'])

            return True

        except Exception as e:
            self.logging.error(e)

            return False

    def describe_table(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            wait_until_exists=True):
        try:
            if wait_until_exists:
                if not self.wait_until_table(
                        access_key_id=access_key_id,
                        secret_access_key=secret_access_key,
                        region_name=region_name,
                        table_name=table_name,
                        exists=True):
                    return False

            dynamodb = boto3.client(
                service_name='dynamodb',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name)

            describe = dynamodb.describe_table(TableName=table_name)

            return describe

        except Exception as e:
            self.logging.error(e)

            return False

    def remove_table(
            self,
            access_key_id,
            secret_access_key,
            region_name,
            table_name,
            wait_until_not_exists=True):
        try:
            dynamodb = boto3.client(
                service_name='dynamodb',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name)

            deleted = dynamodb.delete_table(TableName=table_name)

            if not deleted:
                return False

            if wait_until_not_exists:
                if not self.wait_until_table(
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
