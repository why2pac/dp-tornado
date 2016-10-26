# -*- coding: utf-8 -*-


import boto3

from dp_tornado.engine.helper import Helper as dpHelper


class DynamodbHelper(dpHelper):
    def client(
            self,
            access_key_id,
            secret_access_key,
            region_name):
        return boto3.client(
            service_name='dynamodb',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name)

    def resource(
            self,
            access_key_id,
            secret_access_key,
            region_name):
        return boto3.resource(
            service_name='dynamodb',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name)


