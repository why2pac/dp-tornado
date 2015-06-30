# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2015.06.30
#


from boto.s3.connection import S3Connection
from boto.s3.key import Key


from engine.helper import Helper as dpHelper
from engine.engine import Engine as dpEngine


class S3Bridge(dpEngine):
    def __init__(self, public, secret):
        self.conn = S3Connection(public, secret)

    def bucket(self, bucket_name):
        return self.conn.get_bucket(bucket_name)

    def set_contents_from_file(self, bucket_name, key, fp, url=False):
        fp.seek(0)
        bucket = self.bucket(bucket_name)
        obj = Key(bucket)
        obj.key = key
        res = obj.set_contents_from_file(fp)

        if url:
            return obj.generate_url(0)
        else:
            return res

    def copy(self, from_bucket_name, from_key_name, to_bucket_name, to_key_name):
        from_bucket = self.bucket(from_bucket_name)
        from_key = Key(from_bucket)
        from_key.key = from_key_name

        to_bucket = self.bucket(to_bucket_name)
        return from_key.copy(to_bucket, to_key_name)


class S3Helper(dpHelper):
    def connect(self, public, secret):
        return S3Bridge(public, secret)
