# -*- coding: utf-8 -*-

"""Schema module provides auto-generate relational database model as object based.

File/Class Invoke rules
-----------------------
* */schema/__init__.py*, **DO NOT IMPLEMENT ANY CODE IN THIS FILE**
* */schema/blog/__init__.py*, ``BlogSchema`` > **schema.blog**
* */schema/blog/articles.py*, ``ArticlesSchema`` > **schema.blog.articles**
* */schema/blog/comments.py*, ``CommentsSchema`` > **schema.blog.comments**

Table migration(create or alter) will be executed by invoking ``.migrate()`` method manually.
For example, you can migrate ``comments`` table with invoking ``schema.blog.comments.migrate()`` method.

There are 2 types of schema. One is **__dsn__ specifier** and another one is **table describer**.
``__init__.py`` file of each directory must be **__dsn__ specifier**.
and child ``.py`` files are must be **table describer**.

Here is a **__dsn__ specifier** example **(/schema/blog/__init__.py)**:

.. testcode::

    from dp_tornado.engine.schema import Schema as dpSchema


    class BlogSchema(dpSchema):
        __dsn__ = 'tests.model_test/drv_mysql_test'


and Here is a **table describer** example **(/schema/blog/comments.py)**:

.. testcode::

    from dp_tornado.engine.schema import Table as dpTable
    from dp_tornado.engine.schema import Schema as dpSchema
    from dp_tornado.engine.schema import Attribute as dpAttribute

    class CommentsSchema(dpSchema):
        __table_name__ = 'comments'

        __engine__ = 'InnoDB'
        __charset__ = 'utf8'

        comment_id = dpAttribute.field(dpAttribute.DataType.BIGINT, ai=True, pk=True, nn=True, un=True, comment='Comment ID')
        article_id = dpAttribute.field(dpAttribute.DataType.BIGINT, nn=True, un=True, comment='Parent Article ID')
        author = dpAttribute.field(dpAttribute.DataType.VARCHAR(32), nn=True, comment='Author')
        comment = dpAttribute.field(dpAttribute.DataType.VARCHAR(128), nn=True, comment='Comment')

        primary_key = dpAttribute.index(dpAttribute.IndexType.PRIMARY, 'comment_id')

        idx_articles_author_and_comment = dpAttribute.index(dpAttribute.IndexType.INDEX, ('author', 'comment'))
        idx_articles_comment = dpAttribute.index(dpAttribute.IndexType.INDEX, 'comment')

        fk_comments_article_id = dpAttribute.foreign_key(('article_id', dpSchema.field().blog.articles, 'article_id'))
"""

import inspect

from ..singleton import Singleton as dpSingleton
from ..engine import Engine as dpEngine
from ..loader import Loader as dpLoader
from ..model import Model as dpModel
from ..cache import dpInValueModelConfig


class _ComparableDataType(object):
    name = None
    size = None
    enums = None

    def __eq__(self, other):
        if not other:
            return False

        if self.name == 'ENUM':
            return list(self.enums) == list(other.enums)

        return self.name == other.name and self.size == other.size

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.name == 'ENUM':
            return 'TYPE : %s / ENUMS : %s' % (self.name, list(self.enums))

        return 'TYPE : %s / SIZE : %s' % (self.name, self.size)


class _DataType(object):
    class INT(_ComparableDataType):
        name = 'INT'
        size = 11

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class TINYINT(_ComparableDataType):
        name = 'TINYINT'
        size = 4

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class SMALLINT(_ComparableDataType):
        name = 'SMALLINT'
        size = 6

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class MEDIUMINT(_ComparableDataType):
        name = 'MEDIUMINT'
        size = 9

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class BIGINT(_ComparableDataType):
        name = 'BIGINT'
        size = 20

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class DOUBLE(_ComparableDataType):
        name = 'DOUBLE'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class FLOAT(_ComparableDataType):
        name = 'FLOAT'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class DECIMAL(_ComparableDataType):
        def __init__(self, m=10, d=0):
            self.name = 'DECIMAL'
            self.size = (m, d)

    class CHAR(_ComparableDataType):
        name = 'CHAR'
        size = 1

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class VARCHAR(_ComparableDataType):
        name = 'VARCHAR'
        size = 128

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class TEXT(_ComparableDataType):
        name = 'TEXT'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class TINYTEXT(_ComparableDataType):
        name = 'TINYTEXT'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class MEDIUMTEXT(_ComparableDataType):
        name = 'MEDIUMTEXT'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class LONGTEXT(_ComparableDataType):
        name = 'LONGTEXT'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class ENUM(_ComparableDataType):
        name = 'ENUM'

        def __init__(self, *enums):
            if enums:
                self.enums = enums

    class BLOB(_ComparableDataType):
        name = 'BLOB'
        size = None

        def __init__(self):
            pass

    class LONGBLOB(_ComparableDataType):
        name = 'LONGBLOB'
        size = None

        def __init__(self):
            pass

    class MEDIUMBLOB(_ComparableDataType):
        name = 'MEDIUMBLOB'
        size = None

        def __init__(self):
            pass

    class TINYBLOB(_ComparableDataType):
        name = 'TINYBLOB'
        size = None

        def __init__(self):
            pass

    class DATETIME(_ComparableDataType):
        name = 'DATETIME'
        size = None

        def __init__(self):
            pass

    class DATE(_ComparableDataType):
        name = 'DATE'
        size = None

        def __init__(self):
            pass

    class TIME(_ComparableDataType):
        name = 'TIME'
        size = None

        def __init__(self):
            pass

    class TIMESTAMP(_ComparableDataType):
        name = 'TIMESTAMP'
        size = None

        def __init__(self):
            pass

    class YEAR(_ComparableDataType):
        name = 'YEAR'
        size = 4

        def __init__(self, size=None):
            if size is not None:
                self.size = size

                assert size == 4

    class BINARY(_ComparableDataType):
        name = 'BINARY'
        size = 1

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class VARBINARY(_ComparableDataType):
        name = 'VARBINARY'
        size = 1

        def __init__(self, size=None):
            if size is not None:
                self.size = size


class _IndexType(object):
    class PRIMARY(object):
        pass

    class UNIQUE(object):
        pass

    class FULLTEXT(object):
        pass

    class INDEX(object):
        pass


class Table(object):
    __migrated = False
    __identifier = None
    __thread_stricted = False

    def _get_driver(self):
        dsn = getattr(self, '__dsn__', None)
        dsn_config = dsn.split('/')

        database = dsn_config[1]
        dsn_config = dsn_config[0]

        try:
            package = dsn_config.split('.')
            dsn_conf = dpEngine().config

            for p in package:
                dsn_conf = dsn_conf.__getattr__(p)

            dsn_conf = dsn_conf.databases.__getattr__(database)

        except AttributeError:
            dsn_conf = None

        driver = getattr(dsn_conf, 'driver', None) if dsn_conf else None

        if not dsn_conf or not isinstance(dsn_conf, object):
            raise Exception('The specified dsn is invalid.')

        if driver.startswith('mysql'):
            driver = 'mysql'
        elif driver.startswith('sqlite'):
            driver = 'sqlite'
        else:
            driver = None

        if not driver:
            raise Exception('The specified driver from dsn is not supported.')

        return dsn, driver

    def _guarantee_permission(self):
        if not Table.__thread_stricted:
            return True

        cache_config = dpInValueModelConfig('sqlite', 'static_url', pure=True)
        cache_key = 'dp:engine:schema:permission'

        got = dpEngine().cache.get(cache_key, dsn_or_conn=cache_config)
        gox = Table.__identifier if got else None

        if got:
            if got == gox:
                return True

            if got != gox:
                return False

        identifier = dpEngine().helper.misc.uuid.v1()
        Table.__identifier = identifier

        dpEngine().cache.set(cache_key, identifier, dsn_or_conn=cache_config)
        got = dpEngine().cache.get(cache_key, dsn_or_conn=cache_config)

        if got == identifier:
            return True

        return False

    def migrate(self):
        if not self._guarantee_permission():
            return None

        return self._migrate(migrate_data=True)

    def migrate_schema(self):
        if not self._guarantee_permission():
            return None

        return self._migrate(migrate_data=False)

    def _migrate(self, migrate_data=True):
        if self.__migrated:
            return None

        self.__migrated = True

        fields = sorted(inspect.getmembers(self, lambda o: isinstance(o, Field)), key=lambda o: o[1].__field_priority__)
        indexes = sorted(inspect.getmembers(self, lambda o: isinstance(o, Index)), key=lambda o: o[1].__field_priority__)
        foreign_keys = sorted(inspect.getmembers(self, lambda o: isinstance(o, ForeignKey)), key=lambda o: o[1].__field_priority__)

        for k, v in indexes:
            if v.index_type == Attribute.IndexType.PRIMARY:
                oo = 0
                for e in v.fields:
                    oo += 1
                    o = getattr(self, e)
                    o.pk = oo
                    o.nn = True

        dsn, driver = self._get_driver()

        if driver == 'mysql':
            from .driver.mysql_driver import MySqlDriver as SchemaDriver
        elif driver == 'sqlite':
            from .driver.sqlite_driver import SqliteDriver as SchemaDriver
        else:
            from .driver import SchemaDriver

        return SchemaDriver.migrate(dsn, self, fields, indexes, foreign_keys, migrate_data=migrate_data)

    def migrate_data(self):
        if not self._guarantee_permission():
            return None

        return self._migrate_data()

    def _migrate_data(self):
        dsn, driver = self._get_driver()

        if driver == 'mysql':
            from .driver.mysql_driver import MySqlDriver as SchemaDriver
        elif driver == 'sqlite':
            from .driver.sqlite_driver import SqliteDriver as SchemaDriver
        else:
            from .driver import SchemaDriver

        return SchemaDriver.migrate_data(dsn, self)

    def __getattribute__(self, item):
        o = super(Table, self).__getattribute__(item)

        if isinstance(o, PirorityData):
            setattr(o, '__table__', self)

        return o

    def __setattr__(self, key, value):
        return super(Table, self).__setattr__(key, value)


__PriorityDataCompareIgnoreKeys__ = ['pk', 'query', 'name', 'm_pk']


class PirorityData(object):
    __field_priority__ = 0

    def __init__(self, **kwargs):
        Field.__field_priority__ += 1
        self.__field_priority__ = Field.__field_priority__

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.__temp = kwargs

    def __str__(self):
        return str(self.__temp)

    def __eq__(self, other):
        for k, v in self.__temp.items():
            if k in __PriorityDataCompareIgnoreKeys__:
                continue

            ov = getattr(other, k, None)

            if dpEngine().helper.misc.type.check.string(v):
                if dpEngine().helper.string.cast.unicode(v) != dpEngine().helper.string.cast.unicode(ov):
                    return False
                else:
                    continue

            if ov != v:
                if k == 'nn':
                    ov = getattr(other, 'm_pk', None)

                    if ov == v:
                        continue

                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class Field(PirorityData):
    pass


class Index(PirorityData):
    pass


class ForeignKey(PirorityData):
    pass


class Schema(dpEngine, dpLoader, dpSingleton):
    @staticmethod
    def field():
        return dpEngine().schema


class Attribute(object):
    DataType = _DataType
    IndexType = _IndexType

    @staticmethod
    def field(data_type,
              default=None,
              comment='',
              m_pk=None,
              pk=None,
              uq=None,
              nn=None,
              un=None,
              zf=None,
              ai=None,
              name=None,
              query=None):
        return Field(
            name=name,
            data_type=data_type,
            default=default,
            comment=comment,
            m_pk=m_pk,
            pk=pk,
            uq=uq,
            nn=True if ai else nn,
            un=un,
            zf=zf,
            ai=ai,
            query=query)

    @staticmethod
    def index(index_type, fields, name=None):
        return Index(
            name=name,
            index_type=index_type,
            fields=fields if isinstance(fields, (list, tuple)) else (fields, ))

    @staticmethod
    def foreign_key(fields, on_delete='NO ACTION', on_update='NO ACTION', name=None):
        return ForeignKey(
            name=name,
            on_delete=on_delete,
            on_update=on_update,
            fields=fields if isinstance(fields, (list, tuple)) else (fields, ))

