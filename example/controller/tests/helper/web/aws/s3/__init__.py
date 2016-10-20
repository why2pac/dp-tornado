# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class S3Controller(Controller):
    def get(self):
        # PREPARE
        content = 'aws-s3-test'

        filepath = 'aws'
        filename = 'temp_%s.txt' % self.helper.datetime.timestamp.now()

        s3_key = 'foo/bar/%s' % filename

        self.helper.io.file.remove(filepath)
        assert self.helper.io.file.mkdir(filepath)

        self.helper.io.file.write('%s/%s' % (filepath, filename), content)

        # UPLOAD

        with open('%s/%s' % (filepath, filename), 'rb') as fp:
            uploaded = self.helper.web.aws.s3.upload(
                src=fp,
                dest=s3_key,
                access_key_id=self.ini.static.aws_id,
                secret_access_key=self.ini.static.aws_secret,
                bucket_name=self.ini.static.aws_bucket,
                region_name=self.ini.static.aws_region)

            assert uploaded

        # DOWNLOAD

        download_path = '%s/download_%s' % (filepath, filename)

        downloaded = self.helper.web.aws.s3.download(
            src=s3_key,
            dest=download_path,
            access_key_id=self.ini.static.aws_id,
            secret_access_key=self.ini.static.aws_secret,
            bucket_name=self.ini.static.aws_bucket,
            region_name=self.ini.static.aws_region)

        assert downloaded

        with open(download_path, 'r') as fp:
            assert fp.read() == content

        self.helper.io.file.remove(filepath)
