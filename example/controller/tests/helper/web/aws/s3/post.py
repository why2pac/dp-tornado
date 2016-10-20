# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class PostController(Controller):
    def get(self):
        payload = self.helper.web.aws.s3.generate_presigned_post(
            key='foo/bar/baz.tmp',
            success_action_redirect='http://127.0.0.1/uploaded',
            content_length_range=(10, 1024),
            access_key_id=self.ini.static.aws_id,
            secret_access_key=self.ini.static.aws_secret,
            bucket_name=self.ini.static.aws_bucket,
            region_name=self.ini.static.aws_region)

        assert 'action' in payload
        assert self.helper.web.url.validate(payload['action'])

        self.finish(payload)
