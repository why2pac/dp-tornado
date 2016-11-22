# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class ArticleModel(dpModel):
    def index(self):
        self.schema.bbs.articles.migrate()

    def inquiry(self, article_id=None, page=1, rpp=30):
        where_query = '1 = 1'
        params = []

        if article_id:
            where_query = '{w} AND `article_id` = ?'.replace('{w}', where_query)
            params.append(article_id)

        count = self.scalar("""
            SELECT
                COUNT(*)
            FROM
                `articles`
            WHERE
                {w}
        """.replace('{w}', where_query), params or None, 'db/service')

        params.append(rpp)
        params.append(rpp * (page - 1))

        items = self.rows("""
            SELECT
                *
            FROM
                `articles`
            WHERE
                {w}
            ORDER BY
                `signdate` DESC
            LIMIT ? OFFSET ?
        """.replace('{w}', where_query), params, 'db/service')

        if rpp == 1:
            return items[0] if items else None

        return {
            'page': page,
            'rpp': rpp,
            'count': count,
            'rows': items
        }

    def post(self, author, title, content):
        executed = self.execute("""
            INSERT INTO `articles`
                (`author`, `title`, `content`, `signdate`)
                    VALUES (?, ?, ?, ?)
        """, (author, title, content, self.helper.datetime.timestamp.now()), 'db/service')

        return executed.rowcount
