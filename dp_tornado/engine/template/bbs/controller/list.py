# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller as dpController


class ListController(dpController):
    def get(self, article_id=None):
        if article_id:
            return self.get_view(article_id)

        validate = self.helper.validator.form.validate(self, {
            'page': {'default': 1, 'cast': self.helper.misc.type.int, 'required': False},
            'rpp': {'default': 10, 'cast': self.helper.misc.type.int, 'required': False}
        }, error_res='code')

        if not validate:
            return False

        params = {
            'articles': self.model.article.inquiry(**validate),
        }

        self.render('bbs/list.html', params)

    def get_view(self, article_id):
        article = self.model.article.inquiry(article_id=article_id, rpp=1)

        if not article:
            return self.finish_with_error(404)

        params = {
            'request_uri': self.get_argument('request_uri'),
            'article': article
        }

        self.render('bbs/view.html', params)
