# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Schema as dpSchema
from dp_tornado.engine.schema import Attribute as dpAttribute


class StudentsSchema(dpTable):
    __table_name__ = 'students'

    idx = dpAttribute.field(dpAttribute.DataType.BIGINT, ai=True, comment='Index of Student')
    class_id = dpAttribute.field(dpAttribute.DataType.BIGINT, nn=True, comment='Class ID of Student')
    name = dpAttribute.field(dpAttribute.DataType.VARCHAR(32), name='student_name', nn=True, comment='Name of Student')
    grade = dpAttribute.field(dpAttribute.DataType.ENUM('A', 'B', 'C', 'D', 'F'), nn=True, comment='Grade')
    birthday = dpAttribute.field(dpAttribute.DataType.CHAR(8), nn=True, comment='생년월일')
    admission_year = dpAttribute.field(dpAttribute.DataType.SMALLINT, nn=True, comment='입학연도')

    primary_key = dpAttribute.index(dpAttribute.IndexType.PRIMARY, 'idx')

    index_name = dpAttribute.index(dpAttribute.IndexType.INDEX, 'name')
    index_admission_year_name = dpAttribute.index(dpAttribute.IndexType.INDEX, ('admission_year', 'name'))

    fk_class_id = dpAttribute.foreign_key(('class_id', dpSchema.field().school.classes, 'idx'))
