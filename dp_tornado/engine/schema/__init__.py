# -*- coding: utf-8 -*-


import inspect

from ..singleton import Singleton as dpSingleton
from ..engine import Engine as dpEngine
from ..loader import Loader as dpLoader
from ..model import Model as dpModel


class _DataType(object):
    class INT(object):
        name = 'INT'
        size = 11

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class TINYINT(object):
        name = 'TINYINT'
        size = 4

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class SMALLINT(object):
        name = 'SMALLINT'
        size = 6

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class MEDIUMINT(object):
        name = 'MEDIUMINT'
        size = 9

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class BIGINT(object):
        name = 'BIGINT'
        size = 20

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class DOUBLE(object):
        name = 'DOUBLE'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class FLOAT(object):
        name = 'FLOAT'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class DECIMAL(object):
        def __init__(self, m=10, d=0):
            self.name = 'DECIMAL'
            self.size = (m, d)

    class CHAR(object):
        name = 'CHAR'
        size = 1

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class VARCHAR(object):
        name = 'VARCHAR'
        size = 128

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class TEXT(object):
        name = 'TEXT'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class TINYTEXT(object):
        name = 'TINYTEXT'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class MEDIUMTEXT(object):
        name = 'MEDIUMTEXT'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class LONGTEXT(object):
        name = 'LONGTEXT'
        size = None

        def __init__(self, size=None):
            if size is not None:
                self.size = size

    class ENUM(object):
        name = 'ENUM'

        def __init__(self, *enums):
            if enums:
                self.enums = enums


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

    def migrate(self):
        if self.__migrated:
            return True

        self.__migrated = True

        fields = sorted(inspect.getmembers(self, lambda o: isinstance(o, Field)), key=lambda o: o[1].__field_priority__)
        indexes = sorted(inspect.getmembers(self, lambda o: isinstance(o, Index)), key=lambda o: o[1].__field_priority__)
        foreign_keys = sorted(inspect.getmembers(self, lambda o: isinstance(o, ForeignKey)), key=lambda o: o[1].__field_priority__)

        for k, v in indexes:
            if v.index_type == Attribute.IndexType.PRIMARY:
                for e in v.fields:
                    o = getattr(self, e)
                    o.pk = True

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
        else:
            driver = None

        if not driver:
            raise Exception('The specified driver from dsn is not supported.')

        if driver == 'mysql':
            from .driver.mysql_driver import MySqlDriver as SchemaDriver
        else:
            from .driver import SchemaDriver

        SchemaDriver.migrate(dsn, self, fields, indexes, foreign_keys)

    def __getattribute__(self, item):
        o = super(Table, self).__getattribute__(item)

        if isinstance(o, PirorityData):
            setattr(o, '__table__', self)

        return o

    def __setattr__(self, key, value):
        return super(Table, self).__setattr__(key, value)


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
              comment=None,
              pk=None,
              uq=None,
              nn=None,
              un=None,
              zf=None,
              ai=None,
              name=None):
        return Field(
            name=name,
            data_type=data_type,
            default=default,
            comment=comment,
            pk=pk,
            uq=uq,
            nn=nn,
            un=un,
            zf=zf,
            ai=ai)

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

