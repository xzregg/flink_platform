# -*- coding: utf-8 -*-
# @Time    : 2021-01-06 12:11
# @Author  : xzr
# @File    : flink_job
# @Software: PyCharm
# @Contact :
# @Desc    :
import datetime
import json
import logging
import os
from dataclasses import dataclass

from django.db import models
from django.utils.translation import ugettext_lazy as _
from framework.models import BaseModel, ObjectDictField
from framework.serializer import ConfigOptionSerializer, DataSerializer, s
from framework.utils import DATETIMEFORMAT, ObjectDict, timestamp_to_datetime_str, trace_msg
from framework.utils.cache import CacheAttribute
from framework.utils.myenum import Enum
from framework.validators import LetterValidator
from furl import furl

from myadmin.models.user import User
from .paragraph import CodeParagraph
from .project import Project
from ..job_engine import BaseFlinkJobEngine, EngineStateCode
from ..settings import FLINK_JOB_ENGINE, FLINK_SAVEPOINT_ROOT_PATH


class FlinkConfigTpl(object):
    code_prefix = '%flink.conf'
    text = '''#全局任务 https://ci.apache.org/projects/flink/flink-docs-release-1.12/zh/deployment/config.html
restart-strategy fixed-delay
restart-strategy.fixed-delay.attempts 3
restart-strategy.fixed-delay.delay 20s
state.checkpoints.num-retained 3 
execution.checkpointing.tolerable-failed-checkpoints 3
# 设置任务使用的时间属性是eventtime
pipeline.time-characteristic EventTime
# 设置checkpoint的时间间隔
execution.checkpointing.interval 5min
# 确保检查点之间的间隔
execution.checkpointing.min-pause 1min
# 设置checkpoint的超时时间
execution.checkpointing.timeout 10min
# 设置任务取消后保留hdfs上的checkpoint文件
execution.checkpointing.externalized-checkpoint-retention RETAIN_ON_CANCELLATION
execution.savepoint.ignore-unclaimed-state true
#taskmanager.memory.process.size 1024mb

    '''


TASK_SQL_TEMPLATE = """
-- 任务优化参数 https://ci.apache.org/projects/flink/flink-docs-release-1.12/dev/table/config.html
set table.dynamic-table-options.enabled=True;
set table.optimizer.distinct-agg.split.enabled=True;
set table.exec.mini-batch.enabled=True;
set table.exec.mini-batch.allow-latency=5s;
set table.exec.mini-batch.size=5000;
set table.exec.state.ttl=2d;
"""


class FlinkTableConfigTpl(object):
    code_prefix = '%flink'
    text = '''// 额外执行代码 变量参考 http://zeppelin.apache.org/docs/0.9.0/interpreter/flink.html#paragraph-local-properties
// https://ci.apache.org/projects/flink/flink-docs-stable/zh/dev/table/streaming/query_configuration.html

import org.apache.flink.api.common.time.Time
val env = senv
val tableEnv = stenv
val tConfig: TableConfig = tableEnv.getConfig
val configuration = tConfig.getConfiguration()
// 设置 State TTL
//tConfig.setIdleStateRetentionTime(Time.hours(24), Time.hours(48))
//configuration.setString("execution.checkpointing.interval", "2min")
//configuration.setString("execution.checkpointing.min-pause", "1min")
//configuration.setString("execution.checkpointing.timeout", "10min")
'''


@dataclass
class ConfigOptionItem:
    key: str = ''
    type: type = None
    default: str = ''
    describe: str = ''
    choices: list = None

    def __str__(self):
        return self.key


class ParagraphProperties(ConfigOptionSerializer):
    refreshInterval = s.IntegerField(label=_('刷新时间'), default=5000, help_text=_(
            'Used in `%flink.ssql` to specify frontend refresh interval for streaming data visualization.'))

    parallelism = s.IntegerField(label=_('并行数'), default=2, help_text=_('specify the flink sql job parallelism'))

    maxParallelism = s.IntegerField(label=_('最大并行数'), default=32768,
                                    help_text=_('specify the flink sql job parallelism'))

    savepointDir = s.CharField(label=_('记录点保存目录'), allow_blank=True, default='', help_text=_(
            'If you specify it, then when you cancel your flink job in Zeppelin, it would also do savepoint and store state in this directory. And when you resume your job, it would resume from this savepoint.'))

    resumeFromSavepoint = s.BooleanField(label=_('是否从保存目录恢复'), default=False,
                                         help_text=_('Resume flink job from savepoint if you specify savepointDir.'))

    runAsOne = s.BooleanField(label=_('一个任务执行所有SQL'), default=False,
                              help_text=_('All the insert into sql will run in a single flink job if this is true.'))

    resumeFromLatestCheckpoint = s.BooleanField(label=_('是否从上次 CheckPonit 还原'), default=False, help_text=_(
            'Resume flink job from latest checkpoint if you enable checkpoint.'))

    executionSavepoint = s.CharField(label=_('任务还原点路径'), default='',
                                     help_text=_('execution.savepoint.path'))
    # 重新绑定 字段名
    executionSavepoint.bind('execution.savepoint.path', None)


class TaskTypes(CodeParagraph.TagType):
    Config = 'config', _('Flink Job 全局配置')
    TableConfig = 'table_config', _('Flink Table 配置')
    MainTask = 'task', _('Flink 主要任务')


class FlinkJob(BaseModel):
    """
        Flink Job
    """

    class Status(Enum):
        Ready = 'READY', _('预备')
        Abort = 'ABORT', _('中止')
        Error = 'ERROR', _('错误')
        Finished = 'FINISHED', _('完成')
        Pending = 'PENDING', _('启动中')
        Running = 'RUNNING', _('运行中')

    class Mode(Enum):
        BatchSql = 0, _('批模式')
        StreamSql = 1, _('流模式')

    author = models.ForeignKey(User, verbose_name=_('作者'), on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, verbose_name=_('所属项目'), on_delete=models.CASCADE, null=True)
    name = models.CharField(_('任务名'), max_length=100, null=False, blank=False, validators=[LetterValidator],
                            unique=True)

    alias = models.CharField(_('任务简称'), max_length=100, default='', null=True, blank=True)
    status = models.CharField(_('任务状态'), max_length=10, choices=Status.member_list(), default=Status.Ready)

    job_id = models.CharField(_('任务ID'), max_length=100, default='', null=True, blank=True, db_index=True)

    flink_job_id = models.CharField(_('Flink Job ID'), max_length=100, null=True, blank=True, db_index=True)
    flink_job_url = models.CharField(_('Flink Job Url'), max_length=200, null=True, blank=True, default='')

    mode = models.IntegerField(_('任务模式'), choices=Mode.member_list(), default=Mode.StreamSql)
    cron = models.CharField(_('cron 定时执行'), max_length=100, null=True, blank=True, default='')
    start_datetime = models.DateTimeField(_('任务开始执行时间'), null=True, blank=True)
    stop_datetime = models.DateTimeField(_('任务停止执行时间'), null=True, blank=True)
    remark = models.TextField(_('任务备注'), null=True, blank=True)

    code_paragraphs = models.ManyToManyField(CodeParagraph, verbose_name=_('引用代码段落'), blank=True)

    task_code_type = models.CharField(_('任务 类型'), max_length=20, choices=CodeParagraph.LanguageType.member_list(),
                                      null=False, blank=False, default=CodeParagraph.LanguageType.Sql)
    task_content = models.TextField(_('任务 内容'), null=False, blank=False, default=TASK_SQL_TEMPLATE)

    flink_config = models.TextField(_('flink config 配置'), null=True, blank=True, default=FlinkConfigTpl.text)
    flink_table_config = models.TextField(_('flink table config 配置'), null=True, blank=True,
                                          default=FlinkTableConfigTpl.text)

    status_info = ObjectDictField(_('状态信息'), null=True, blank=True,
                                  default={})  # {'task':{"id":"paragraph_1610440281242_1472177900","status":"READY","progress":"0"},'config':...}

    task_properties = ObjectDictField(_('任务属性'), null=True, blank=True,
                                      default=ParagraphProperties.default_map)

    last_execution_savepoint = models.CharField(_('最后 savepoint 路径'), max_length=2000, null=True, blank=True)
    execution_savepoint_path = models.CharField(_('启动 savepoint 路径'), max_length=2000, null=True, blank=True,
                                                default='')

    @property
    def author_alias(self):
        return self.author.alias if self.author else ''

    @property
    def project_alias(self):
        return self.project.alias if self.project else ''

    def set_status_info(self, status_info):
        if isinstance(status_info, str):
            status_info = json.loads(status_info)
        status_info = FlinkJobStatusInfoSerializer(data={'status_info': status_info})
        status_info.o.engine_url = self.job_engine.get_engine_url()
        self.status_info = status_info.data

        return self.status_info

    def get_status_info(self):
        return self.status_info

    def get_task_properties(self):
        return self.task_properties

    def save(self, is_sync_engine=False, *args, **kwargs):
        if not self.alias:
            self.alias = self.name
        super(FlinkJob, self).save(*args, **kwargs)
        if is_sync_engine:
            self.sync_engine_job()

    def sync_engine_job(self):
        job_id = self.job_engine.save_job()
        if job_id and not self.job_id:
            self.job_id = job_id
            self.save(is_sync_engine=False)
        return self

    def delete(self, *args, **kwargs):
        if self.job_id:
            state = self.job_engine.stop(True)
            if state.code == EngineStateCode.SUCCESS:
                self.job_engine.delete_job()

        super().delete(*args, **kwargs)

    def update_last_execution_savepoint(self):
        self.last_execution_savepoint = self.job_engine.get_last_savepoint_path()

    def update_job_url(self):
        self.flink_job_url = self.job_engine.get_flink_job_url()

    def update_job_id(self):
        self.flink_job_id = self.job_engine.get_flink_job_id()

    def update_status_info(self):
        """
        更新任务状态
        :return:
        """
        try:
            status_info_map = self.job_engine.status_info
            old_status = self.status
            self.update_job_url()
            self.update_job_id()
            self.update_last_execution_savepoint()
            self.job_engine.update_main_task_status()
            self.set_status_info(status_info_map)
            for k, status_info in status_info_map.items():
                task_status = status_info.get('status', 'ERROR')
                self.status = self.Status(task_status)
                if self.status in [self.Status.Error,self.Status.Finished]:
                    self.stop_datetime = datetime.datetime.now()
                # 非完成的状态
                if not task_status in [self.Status.Finished, self.Status.Running]:
                    break
        except Exception as e:
            self.status = self.Status.Error
            logging.error(e.args[0])
            self.set_status_info(
                    {'status_info': {TaskTypes.MainTask: {'status': self.Status.Error, 'errorMessage': e.args[0]}}})
        self.save(is_sync_engine=False)

    def get_savepoint_path(self):
        return os.path.join(self.get_job_storage_path(), 'savepoints')

    def get_checkponit_path(self):
        return os.path.join(self.get_job_storage_path(), 'checkpoints')

    def get_job_storage_path(self):
        return os.path.join(FLINK_SAVEPOINT_ROOT_PATH, self.name)

    @CacheAttribute
    def code_paragraph_list(self):
        return self.code_paragraphs.all() if self.id else []

    # 合成
    # compile
    def get_storage_file_list(self):
        from ..settings import FLINK_SAVEPOINT_PATH_BACKEND_ADDRESS
        import hdfs
        storage_file_backed = hdfs.Client(FLINK_SAVEPOINT_PATH_BACKEND_ADDRESS, timeout=10)
        storage_file_list = self.get_storage_file_list_status(storage_file_backed, 'savepoints',
                                                              self.get_savepoint_path())
        # storage_file_list = self.get_storage_file_list_status(FLINK_SAVEPOINT_PATH_BACKEND, 'checkponits',
        #                                                       self.get_checkponit_path())
        storage_file_list.sort(key=lambda x: x.modification_time, reverse=True)

        return storage_file_list

    def get_storage_file_list_status(self, backend, type_name, path):
        path_obj = furl(path)
        path = path_obj.pathstr
        origin = furl(self.last_execution_savepoint).origin
        data_list = []
        try:
            for dir_name, dir_status in backend.list(path, status=True):
                data: FlinkStorageFileSerializer = ObjectDict()
                data.dir_path = origin + os.path.join(path, dir_name)
                data.storage_type = type_name
                data.owner = dir_status.get('owner', '')
                data.modification_time = timestamp_to_datetime_str(dir_status.get('modificationTime', 1000) / 1000)
                data_list.append(data)
        except Exception as e:
            logging.error(trace_msg())
        return data_list

    def get_source(self):
        return [c for c in self.code_paragraph_list if c.tag == CodeParagraph.TagType.Source]

    def get_slink(self):
        return [c for c in self.code_paragraph_list if c.tag == CodeParagraph.TagType.Slink]

    def get_udf(self):
        return [c for c in self.code_paragraph_list if c.tag == CodeParagraph.TagType.Udf]

    def get_flink_config_text(self):
        return self.flink_config

    def get_flink_table_config(self):
        return self.flink_table_config

    def get_job_content(self):
        return self.job_content

    _job_engine = None

    @property
    def job_engine(self) -> BaseFlinkJobEngine:
        from framework.utils import import_func
        if self._job_engine is None:
            engine_class_path = '%s.%s' % (self.get_app_name(), FLINK_JOB_ENGINE)
            engine_class = import_func(engine_class_path)
            _self = self
            self._job_engine = engine_class(flink_job_model=_self)
        return self._job_engine

    def start(self, use_last_savepoint=True):
        if use_last_savepoint:
            savepoint_path = self.last_execution_savepoint
        else:
            savepoint_path = self.execution_savepoint_path.strip()
        if self.status != self.Status.Running:
            state = self.job_engine.start(savepoint_path)
            if state.code == EngineStateCode.SUCCESS:
                self.status = self.Status.Running
                self.start_datetime = datetime.datetime.now()
                self.stop_datetime = None
                self.execution_savepoint_path = savepoint_path
            else:
                self.status = self.Status.Abort
            self.update_status_info()
            return state

    def restart(self, force=False, use_last_savepoint=True):
        state = self.stop(force)
        if state.code == EngineStateCode.SUCCESS:
            self.start(use_last_savepoint)
        return state

    def stop(self, force=False):
        state = self.job_engine.stop(force)
        if state.code == EngineStateCode.SUCCESS:
            self.status = self.Status.Abort
            self.stop_datetime = datetime.datetime.now()
            self.start_datetime = None
        self.update_status_info()
        return state


class FlinkTaskStatusInfoSerializer(DataSerializer):
    """Flink task 状态信息"""
    id = s.CharField(label=_('Task id'), required=False)
    status = s.ChoiceField(label=_('状态'), choices=FlinkJob.Status.member_list())
    errorMessage = s.CharField(label=_('错误信息'), required=False)


class FlinkJobStatusSerializer(DataSerializer):
    config = FlinkTaskStatusInfoSerializer(required=False)
    source = FlinkTaskStatusInfoSerializer(required=False)
    slink = FlinkTaskStatusInfoSerializer(required=False)
    udf = FlinkTaskStatusInfoSerializer(required=False)
    table_config = FlinkTaskStatusInfoSerializer(required=False)
    task = FlinkTaskStatusInfoSerializer(required=False)


class FlinkJobStatusInfoSerializer(DataSerializer):
    """
    Flink Job 状态信息
    """
    status_info = FlinkJobStatusSerializer(label=_('任务状态信息'), required=False)
    engine_url = s.CharField(label=_('任务引擎地址'), required=False)


class FlinkStorageFileSerializer(DataSerializer):
    """任务保存点信息"""
    dir_path = s.CharField(label=_('路径'), required=True)
    storage_type = s.CharField(label=_('保存点类型'), required=True)
    owner = s.CharField(label=_('所有者'), required=True)
    size = s.IntegerField(label=_('目录大小'), required=False)
    modification_time = s.DateTimeField(label=_('目录修改时间'), format=DATETIMEFORMAT, required=True)


class FlinkStorageFileListSerializer(DataSerializer):
    """"""
    points = FlinkStorageFileSerializer(label='保存点', many=True)


class FlinkJobGroup(BaseModel):
    name = models.CharField(_('任务组名'), max_length=100, null=False, blank=False, validators=[LetterValidator],
                            db_index=True)
    author = models.ForeignKey(User, verbose_name=_('作者'),on_delete=models.DO_NOTHING)
    parent = models.ForeignKey(to='self', verbose_name=_("上级"), on_delete=models.DO_NOTHING, null=True)
    alias = models.CharField(_('任务组描述'), max_length=100, null=False, blank=False)
    jobs = models.ManyToManyField(FlinkJob, _('任务'))
