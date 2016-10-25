# -*- coding: utf-8 -*-


import io
import boto3

from dp_tornado.engine.helper import Helper as dpHelper


class S3Helper(dpHelper):
    def upload(self,
               src,
               dest,
               access_key_id,
               secret_access_key,
               bucket_name,
               region_name,
               uploaded_check=True,
               ExtraArgs=None):
        if self.helper.misc.type.check.string(src):
            if not self.helper.io.file.is_file(src):
                return False
        elif self.helper.misc.system.py_version <= 2 and not isinstance(src, file):
            return False
        elif self.helper.misc.system.py_version >= 3 and not isinstance(src, io.IOBase):
            return False

        s3 = boto3.client(
            service_name='s3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)

        if self.helper.misc.type.check.string(src):
            s3.upload_file(src, bucket_name, dest, ExtraArgs=ExtraArgs)
        elif src:
            s3.upload_fileobj(src, bucket_name, dest, ExtraArgs=ExtraArgs)

        if uploaded_check:
            return self.exists(
                key=dest,
                access_key_id=access_key_id,
                secret_access_key=secret_access_key,
                bucket_name=bucket_name,
                region_name=region_name)

        return True

    def download(self,
                 src,
                 dest,
                 access_key_id,
                 secret_access_key,
                 bucket_name,
                 region_name,
                 **kwargs):
        s3 = boto3.client(
            service_name='s3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)

        self.helper.io.file.mkdir(self.helper.io.file.dirname(dest))
        s3.download_file(bucket_name, src, dest, ExtraArgs=kwargs)

        return True if self.helper.io.file.is_file(dest) else False

    def copy(self,
             region_name,
             src_bucket_name,
             src_key,
             dest_bucket_name,
             dest_key,
             access_key_id,
             secret_access_key,
             copied_check=True):
        import boto3

        s3 = boto3.client(
            service_name='s3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)

        copy_source = {
            'Bucket': src_bucket_name,
            'Key': src_key
        }

        s3.copy(copy_source, dest_bucket_name, dest_key)

        if copied_check:
            return self.exists(
                key=dest_key,
                access_key_id=access_key_id,
                secret_access_key=secret_access_key,
                bucket_name=dest_bucket_name,
                region_name=region_name)

        return True

    def browse(self, access_key_id, secret_access_key, region_name, bucket_name, prefix):
        try:
            s3 = boto3.client(
                service_name='s3',
                region_name=region_name,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key)

            result = s3.list_objects(Bucket=bucket_name, Prefix=prefix)

            if 'Contents' not in result:
                return []

            contents = []

            for e in result['Contents']:
                if 'Key' not in e or 'Size' not in e:
                    continue

                attrs = {
                    'Size': e['Size'],
                    'LastModified': e['LastModified'] if 'LastModified' in e else None,
                    'StorageClass': e['StorageClass'] if 'StorageClass' in e else None,
                    'ETag': e['ETag'] if 'ETag' in e else None
                }

                contents.append((e['Key'], attrs))

            return contents

        except Exception as e:
            self.logging.exception(e)

            return False

    def exists(self, key, access_key_id, secret_access_key, bucket_name, region_name):
        s3 = boto3.client(
            service_name='s3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)

        try:
            return True if s3.head_object(Bucket=bucket_name, Key=key) else False
        except Exception:
            return False

    def generate_presigned_post(self,
                                key,
                                access_key_id,
                                secret_access_key,
                                bucket_name,
                                region_name,
                                success_action_redirect=None,
                                content_length_range=None,
                                max_content_length=None,
                                expires_in=6000,
                                acl=None):
        s3 = boto3.client(
            service_name='s3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)

        fields = {}
        conditions = []

        if success_action_redirect:
            fields['success_action_redirect'] = success_action_redirect
            conditions.append({'success_action_redirect': success_action_redirect})
        else:
            fields['success_action_status'] = '201'
            conditions.append({'success_action_status': '201'})

        if acl:
            conditions.append({'acl': acl})

        if content_length_range and len(content_length_range) == 2:
            conditions.append(["content-length-range", content_length_range[0], max_content_length])
        elif max_content_length:
            conditions.append(["content-length-range", 0, max_content_length])

        payload = s3.generate_presigned_post(
            Bucket=bucket_name,
            Key=key,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expires_in)

        return {
            'action': payload['url'],
            'fields': [{'name': k, 'value': v} for k, v in payload['fields'].items()]
        }
