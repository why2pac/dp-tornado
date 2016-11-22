# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Attribute as dpAttribute


class ArticlesSchema(dpTable):
    __table_name__ = 'articles'

    article_id = dpAttribute.field(dpAttribute.DataType.INT, ai=True, pk=True, nn=True, un=True, comment='Article ID')
    title = dpAttribute.field(dpAttribute.DataType.VARCHAR(128), nn=True, comment='Title')
    content = dpAttribute.field(dpAttribute.DataType.LONGTEXT, nn=True, comment='Content')
    author = dpAttribute.field(dpAttribute.DataType.VARCHAR(64), comment='Author')
    signdate = dpAttribute.field(dpAttribute.DataType.INT, comment='Signdate')

    idx_articles_title = dpAttribute.index(dpAttribute.IndexType.INDEX, 'title')
    idx_articles_author = dpAttribute.index(dpAttribute.IndexType.INDEX, 'author')
    idx_articles_signdate = dpAttribute.index(dpAttribute.IndexType.INDEX, 'signdate')

    __dummy_data__ = [
        {'article_id': 1, 'title': 'Helloworld!', 'content': 'Hello!', 'author': 'James', 'signdate': 1478772800},
        {'article_id': 2, 'title': 'Hi!', 'content': 'Hi! Nice to meet you!', 'author': 'Amber', 'signdate': 1478782800},
        {'article_id': 3, 'title': 'Nice to meet you!', 'content': 'Hello. Nice to meet you!', 'author': 'Alice', 'signdate': 1478792800},
        {'article_id': 4, 'title': 'Good morning!', 'content': 'Hi! Good morning!', 'author': 'Elsa', 'signdate': 1478802800},
        {'article_id': 5, 'title': 'Good afternoon!', 'content': 'Hi! Good afternoon!', 'author': 'Kevin', 'signdate': 1478812800},
        {'article_id': 6, 'title': 'Good evening!', 'content': 'Hi! Good evening!', 'author': 'Sam', 'signdate': 1478822800},
        {'article_id': 7, 'title': 'Good night!', 'content': 'Hi! Good night!', 'author': 'Thomas', 'signdate': 1478832800},
        {'article_id': 8, 'title': 'What up!', 'content': 'Hi! What up!', 'author': 'Tim', 'signdate': 1478842800},
        {'article_id': 9, 'title': 'Yo!', 'content': 'Hi! Yo!', 'author': 'William', 'signdate': 1478852800},
        {'article_id': 10, 'title': 'Hor are you?', 'content': 'Hi! What up!', 'author': 'Oscar', 'signdate': 1478862800},
        {'article_id': 11, 'title': 'Good bye!', 'content': 'Hi! Good bye!', 'author': 'Walter', 'signdate': 1478872800},
        {'article_id': 12, 'title': 'See you again!', 'content': 'Hi! See you again!', 'author': 'Jackson', 'signdate': 1478882800},
        {'article_id': 13, 'title': 'Hello!', 'content': 'Hi! What up!', 'author': 'Mike', 'signdate': 1478892800}
    ]
