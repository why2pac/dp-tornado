# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller as dpController


class PostController(dpController):
    def get(self):
        params = {
            'request_uri': self.get_argument('request_uri')
        }

        self.render('bbs/post.html', params)

    def post(self):
        validate = self.helper.validator.form.validate(self, {
            'author': {'required': True},
            'title': {'required': True},
            'content': {'required': True}
        }, error_res='code')

        if not validate:
            return

        if not self.model.article.post(**validate):
            return self.finish_with_error(500)

        self.finish({
            'result': True
        })
