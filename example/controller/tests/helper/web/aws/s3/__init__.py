# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class S3Controller(Controller):
    def get(self):
        for _ in range(3):
            try:
                # PREPARE
                content = 'aws-s3-test'

                filepath = 'aws'
                filename = 'temp_%s.txt' % self.helper.datetime.timestamp.now()

                key_prefix = 'tests/%s' % self.ini.server.identifier
                s3_key = '%s/foo/bar/%s' % (key_prefix, filename)

                self.helper.io.file.remove(filepath)
                assert self.helper.io.path.mkdir(filepath)

                self.helper.io.file.write('%s/%s' % (filepath, filename), content)

                # UPLOAD

                with open('%s/%s' % (filepath, filename), 'rb') as fp:
                    uploaded = self.helper.web.aws.s3.upload(
                        src=fp,
                        dest=s3_key,
                        access_key_id=self.ini.static.aws_id,
                        secret_access_key=self.ini.static.aws_secret,
                        region_name=self.ini.static.aws_region,
                        bucket_name=self.ini.static.aws_bucket)

                    assert uploaded

                # COPY 1

                s3_key_copy = '%s/foo/bar/copy/%s' % (key_prefix, filename)

                copied = self.helper.web.aws.s3.copy(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    src_bucket_name=self.ini.static.aws_bucket,
                    src_key=s3_key,
                    dest_bucket_name=self.ini.static.aws_bucket,
                    dest_key=s3_key_copy)

                assert copied

                # COPY 2

                s3_key_copy_2 = '%s/foo/bar/copy2/%s' % (key_prefix, filename)

                copied = self.helper.web.aws.s3.copy(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    src_bucket_name=self.ini.static.aws_bucket,
                    src_key=s3_key,
                    dest_bucket_name=self.ini.static.aws_bucket,
                    dest_key=s3_key_copy_2)

                assert copied

                # BROWSE

                items = self.helper.web.aws.s3.browse(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    bucket_name=self.ini.static.aws_bucket,
                    prefix='%s/foo/bar/' % key_prefix)

                assert isinstance(items, (list, tuple))
                assert len([e for e in items if len(e) == 2 and e[0] == s3_key]) == 1

                # DOWNLOAD

                download_path = '%s/download_%s' % (filepath, filename)

                downloaded = self.helper.web.aws.s3.download(
                    src=s3_key,
                    dest=download_path,
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    bucket_name=self.ini.static.aws_bucket)

                assert downloaded

                with open(download_path, 'r') as fp:
                    assert fp.read() == content

                self.helper.io.file.remove(filepath)

                # REMOVE

                removed = self.helper.web.aws.s3.remove(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    bucket_name=self.ini.static.aws_bucket,
                    key=s3_key_copy)

                assert len(removed) == 1 and removed[0] == s3_key_copy

                removed = self.helper.web.aws.s3.remove(
                    access_key_id=self.ini.static.aws_id,
                    secret_access_key=self.ini.static.aws_secret,
                    region_name=self.ini.static.aws_region,
                    bucket_name=self.ini.static.aws_bucket,
                    prefix='%s/foo' % key_prefix)

                assert len(removed) == 2 and len([True for e in removed if e in (s3_key_copy_2, s3_key)]) == 2

                return self.finish('done')

            except Exception as e:
                self.logging.exception(e)

                import time
                time.sleep(10)

        return self.finish_with_error(500)
