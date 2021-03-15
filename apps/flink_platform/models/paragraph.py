# -*- coding: utf-8 -*-
# @Time    : 2021-01-06 14:51
# @Author  : xzr
# @File    : paragraph
# @Software: PyCharm
# @Contact : 
# @Desc    : 


from django.db import models
from django.utils.translation import ugettext_lazy as _

from .project import Project
from framework.models import BaseModel, BaseNameModel, ObjectDictField
from framework.utils.myenum import Enum
from framework.utils.sql import get_ddl_table_info
from framework.validators import LetterValidator
from .connector import Connector


class Datalayered(Enum):
    ODS = 'ods', _('原始数据层')
    DWD = 'dwd', _('细粒度数据层')
    DWM = 'dwm', _('轻度汇总数据层')
    DMS = 'dms', _('报表/宽表数据层')
    DIM = 'dim', _('维度数据层')
    APP = 'app', _('应用数据层')


class CodeParagraph(BaseModel):
    """Flink 代码段"""

    class LanguageType(Enum):
        Sql = 'sql', 'SQL'
        Python = 'python', 'Python'
        Scala = 'scala', 'Scala'

    class TagType(Enum):
        Source = 'source', 'Flink Source'
        Slink = 'slink', 'Flink Slink'
        Udf = 'udf', 'Flink Udf'

    project = models.ForeignKey(Project, verbose_name=_('所属项目'), on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(_('段落名'), max_length=100, null=False, blank=False, validators=[LetterValidator],
                            db_index=True, help_text=_('Source 一般为 table name'))
    alias = models.CharField(_('段落显示名'), max_length=100, null=False, blank=True, default='')
    language = models.CharField(_('语言类型'), max_length=20, choices=LanguageType.member_list(), default=LanguageType.Sql)
    tag = models.CharField(_('段落类型标签'), max_length=20, choices=TagType.member_list())

    text = models.TextField(_('代码内容'), default='', null=False, blank=True)

    connector = models.ForeignKey(Connector, verbose_name=_('所属连接器'), on_delete=models.DO_NOTHING, null=True,
                                  blank=True)

    group = models.CharField(_('组'), default='', null=False, blank=True, max_length=100, validators=[LetterValidator])
    is_share = models.BooleanField(_('可共享'), default=True)
    table_schema = ObjectDictField(_('包含的表格信息'), default={})

    @property
    def project_alias(self):
        return self.project.alias if self.project else ''

    def save(self, *args, **kwargs):
        if not self.alias:
            self.alias = self.name
        self.parse_sql_table_schema()
        super(CodeParagraph, self).save(*args, **kwargs)

    def parse_sql_table_schema(self):
        if self.language == self.LanguageType.Sql:
            self.table_schema = get_ddl_table_info(self.text)


class TableColumn(BaseNameModel):
    """表字段定义"""
    relation = models.ManyToManyField(CodeParagraph, verbose_name=_('关联'), blank=True)
    column_type = models.CharField(_('数据类型'), null=False, blank=False, max_length=10)
    column_definition = models.CharField(_('数据类型定义'), max_length=100, default='', null=True, blank=True)
