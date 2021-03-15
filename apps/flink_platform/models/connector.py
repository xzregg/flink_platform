# -*- coding: utf-8 -*-
# @Time    : 2021-01-29 18:40
# @Author  : xzr
# @File    : connector
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 

from __future__ import absolute_import

from framework.models import _, BaseNameModel, models, ObjectDictField
from framework.serializer import ConfigOptionSerializer, s
from framework.utils.myenum import Enum
from .project import Project


class ConnectorPropertiesSerializer(ConfigOptionSerializer):

    def get_ddl_with_properties(self):
        return ',\n'.join(["'%s' = '%s'" % (k, v) for k, v in self.data.items()])


class KafkaConnectorConfigOptionSerializer(ConnectorPropertiesSerializer):
    connector = s.CharField(label=_('连接器类型'), default='kafka')
    properties_bootstrap_servers = s.CharField(label=_('Kakfa 连接地址'), default='')
    properties_bootstrap_servers.bind('properties.bootstrap.servers', None)


class ConnectorType(Enum):
    Kafka = 'kafka', 'Kafka'
    Kudu = 'kudu', 'Kudu'
    Mysql = 'mysql', 'Mysql'
    Redis = 'redis', 'Redis'
    Hive = 'hive', 'Hive'
    MysqlCdc = 'mysql_cdc', 'MysqlCdc'


class Connector(BaseNameModel):
    """Flink 连接器
    # https://ci.apache.org/projects/flink/flink-docs-release-1.12/zh/dev/table/connectors/
    """
    project = models.ForeignKey(Project, verbose_name=_('所属项目'), on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(_('类型'), max_length=10, choices=ConnectorType.member_list(), null=False, blank=False)
    config = ObjectDictField(_('配置'), null=True, blank=True, )

    @property
    def project_alias(self):
        return self.project.alias
