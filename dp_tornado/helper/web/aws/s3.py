# -*- coding: utf-8 -*-


import io
import boto3

from dp_tornado.engine.helper import Helper as dpHelper


class S3Helper(dpHelper):
    def upload(self,
               access_key_id,
               secret_access_key,
               region_name,
               bucket_name,
               src,
               dest,
               uploaded_check=True,
               ExtraArgs=None):
        if self.helper.misc.type.check.string(src):
            if not self.helper.io.path.is_file(src):
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
                access_key_id=access_key_id,
                secret_access_key=secret_access_key,
                region_name=region_name,
                bucket_name=bucket_name,
                key=dest)

        return True

    def download(self,
                 access_key_id,
                 secret_access_key,
                 region_name,
                 bucket_name,
                 src,
                 dest,
                 **kwargs):
        s3 = boto3.client(
            service_name='s3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)

        self.helper.io.path.mkdir(self.helper.io.path.dirname(dest))
        s3.download_file(bucket_name, src, dest, ExtraArgs=kwargs)

        return True if self.helper.io.path.is_file(dest) else False

    def copy(self,
             access_key_id,
             secret_access_key,
             region_name,
             src_bucket_name,
             src_key,
             dest_bucket_name,
             dest_key,
             copied_check=True):
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
                access_key_id=access_key_id,
                secret_access_key=secret_access_key,
                region_name=region_name,
                bucket_name=dest_bucket_name,
                key=dest_key)

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

    def exists(self, key, access_key_id, secret_access_key, region_name, bucket_name):
        s3 = boto3.client(
            service_name='s3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)

        try:
            return True if s3.head_object(Bucket=bucket_name, Key=key) else False
        except Exception:
            return False

    def remove(self, access_key_id, secret_access_key, region_name, bucket_name, key=None, prefix=None, deleted_check=True):
        assert key or prefix
        assert not (key and prefix)

        try:
            s3 = boto3.client(
                service_name='s3',
                region_name=region_name,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key)

            # with specified key, single key
            if key:
                deleted = s3.delete_object(Bucket=bucket_name, Key=key)

                # Check response
                if not deleted or 'ResponseMetadata' not in deleted \
                        or 'HTTPStatusCode' not in deleted['ResponseMetadata'] \
                        or deleted['ResponseMetadata']['HTTPStatusCode'] % 200 > 99:
                    return False

                if deleted_check:
                    if self.exists(
                            access_key_id=access_key_id,
                            secret_access_key=secret_access_key,
                            region_name=region_name,
                            bucket_name=bucket_name,
                            key=key):
                        return False

                return key,

            # with prefix, multiple keys
            elif prefix:
                keys = self.browse(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    bucket_name=self.ini.static.aws_bucket,
                    prefix=prefix)

                if keys is False:
                    return False

                elif not keys:
                    return None

                delete = {'Objects': [{'Key': e[0]} for e in keys]}
                deleted = s3.delete_objects(Bucket=bucket_name, Delete=delete)

                # Check response
                if not deleted or 'Deleted' not in deleted \
                        or 'ResponseMetadata' not in deleted \
                        or 'HTTPStatusCode' not in deleted['ResponseMetadata'] \
                        or deleted['ResponseMetadata']['HTTPStatusCode'] % 200 > 99:
                    return False

                return tuple([e['Key'] for e in deleted['Deleted'] if 'Key' in e])

            return False

        except Exception as e:
            self.logging.exception(e)

            return False

    def generate_presigned_post(self,
                                access_key_id,
                                secret_access_key,
                                region_name,
                                bucket_name,
                                key,
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
