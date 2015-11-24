# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper
from dp_tornado.engine.engine import Engine as dpEngine


_s3_connection_ = None


def s3_connection():
    global _s3_connection_

    if _s3_connection_:
        return _s3_connection_

    try:
        from boto.s3.connection import S3Connection

        import logging
        logging.getLogger('boto').setLevel(logging.CRITICAL)

        _s3_connection_ = S3Connection

    except ImportError as e:
        raise e

    return _s3_connection_


class S3Bridge(dpEngine):
    def __init__(self, public, secret):
        try:
            from boto.s3.connection import S3Connection

            import logging
            logging.getLogger('boto').setLevel(logging.CRITICAL)

        except ImportError as e:
            raise e

        self.conn = S3Connection(public, secret)

    def bucket(self, bucket_name):
        return self.conn.get_bucket(bucket_name)

    def set_contents_from_file(self, bucket_name, key, fp, url=False):
        try:
            from boto.s3.key import Key
        except ImportError as e:
            raise e

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
        try:
            from boto.s3.key import Key
        except ImportError as e:
            raise e

        from_bucket = self.bucket(from_bucket_name)
        from_key = Key(from_bucket)
        from_key.key = from_key_name

        to_bucket = self.bucket(to_bucket_name)
        return from_key.copy(to_bucket, to_key_name)


class S3Helper(dpHelper):
    def connect(self, public, secret):
        return S3Bridge(public, secret)

    def prepare_post(self,
                     aws_access_key_id,
                     aws_secret_access_key,
                     bucket_name,
                     key,
                     success_action_redirect=None,
                     max_content_length=None,
                     expires_in=6000,
                     acl=None):
        s3 = s3_connection()(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)

        if not success_action_redirect:
            fields = [{"name": "success_action_status", "value": "201"}]
            conditions = ['{"success_action_status": "201"}']
        else:
            fields = [{"name": "success_action_redirect", "value": success_action_redirect}]
            conditions = ['{"success_action_redirect": "%s"}' % success_action_redirect]

        payload = s3.build_post_form_args(
            bucket_name=bucket_name,
            key=key,
            expires_in=expires_in,
            acl=acl,
            max_content_length=max_content_length,
            fields=fields,
            conditions=conditions)

        return payload

    def generate_url_with_filename(self,
                                   aws_access_key_id,
                                   aws_secret_access_key,
                                   bucket_name,
                                   key,
                                   file_name,
                                   disposition='attachment',
                                   expires_in=6000):
        s3 = s3_connection()(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)

        response_headers = {
            'response-content-disposition':
                '%s; filename="%s"' % (disposition, self.helper.url.urlencode(self.helper.string.to_str(file_name)))
        }

        return s3.generate_url(expires_in, 'GET', bucket_name, key, response_headers=response_headers)
