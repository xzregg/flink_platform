# -*- coding: utf-8 -*-
# @Time    : 2021-01-07 15:29
# @Author  : xzr
# @File    : zeppelin
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
import datetime
import time
from typing import List

from addict import Dict
from requests.exceptions import Timeout

from framework.utils import OrderedDict
from framework.utils.myenum import Enum
from . import BaseFlinkJobEngine, EngineStateCode
from .zeppelin_pyclient import ZeppelinClient
from ..models.flink_job import FlinkJob, ParagraphProperties, TaskTypes
from ..models.paragraph import CodeParagraph
from ..settings import FLINK_ZEPPELIN_API_ADDRESS, FLINK_ZEPPELIN_API_PASSWORD, FLINK_ZEPPELIN_API_USER

SQL_CODE_PREFIX_MAP = {
        FlinkJob.Mode.BatchSql : '%flink.bsql',
        FlinkJob.Mode.StreamSql: '%flink.ssql',
}

CODE_PREFIX_MAP = {
        CodeParagraph.LanguageType.Python: '%flink.pyflink',
        CodeParagraph.LanguageType.Scala : '%flink',
}
CODE_PREFIX_MAP.update(SQL_CODE_PREFIX_MAP)


class ZeppelinParagraphStatus(Enum):
    READY = 'READY', 'READY'
    ABORT = 'ABORT', 'ABORT'
    ERROR = 'ERROR', 'ERROR'
    FINISHED = 'FINISHED', 'FINISHED'
    PENDING = 'PENDING', 'PENDING'
    RUNNING = 'RUNNING', 'RUNNING'


class FlinkJobEngine(BaseFlinkJobEngine):
    """ Zeppelin Job 提交
    - http://zeppelin.apache.org/docs/0.9.0/interpreter/flink.html
    """
    PARENT_PATH = 'FLINK_PLATFORM_JOB'

    def __init__(self, flink_job_model: FlinkJob):
        super(FlinkJobEngine, self).__init__(flink_job_model)
        self.zc = ZeppelinClient(FLINK_ZEPPELIN_API_ADDRESS, FLINK_ZEPPELIN_API_USER, FLINK_ZEPPELIN_API_PASSWORD,
                                 timeout=180)

    def get_job_mode(self):
        return self.flink_job_model.mode

    def compile_code_prefix(self, task_code_type):
        if task_code_type == CodeParagraph.LanguageType.Sql:
            code_prefix = SQL_CODE_PREFIX_MAP.get(self.flink_job_model.mode)
        else:
            code_prefix = CODE_PREFIX_MAP.get(self.flink_job_model.task_code_type)
        return code_prefix

    def compile_source(self):
        code_prefix = SQL_CODE_PREFIX_MAP.get(self.flink_job_model.mode)
        source_text_list = [code_prefix]
        # 只支持 sql 类的 Source
        for s in self.flink_job_model.get_source():
            if s.language == CodeParagraph.LanguageType.Sql:
                source_text_list.append('\n-- %s\nDROP TABLE IF EXISTS %s;\n%s ' % (s.alias, s.name, s.text))

        return '\n'.join(source_text_list)

    def compile_slink(self):
        code_prefix = SQL_CODE_PREFIX_MAP.get(self.flink_job_model.mode)
        slink_text_list = [code_prefix]
        # 只支持 sql 类的 Slink
        for s in self.flink_job_model.get_slink():
            if s.language == CodeParagraph.LanguageType.Sql:
                slink_text_list.append('\n-- %s \nDROP TABLE IF EXISTS %s;\n%s ' % (s.alias, s.name, s.text))

        return '\n'.join(slink_text_list)

    def compile_flink_config(self):
        code_list = ['%flink.conf',
                     'flink.yarn.appName Zeppelin Flink Session %s' % self.flink_job_model.name,
                     self.flink_job_model.get_flink_config_text()]
        code_list.append('state.checkpoints.dir %s' % self.flink_job_model.get_checkponit_path())
        code_list.append('state.savepoints.dir %s' % self.flink_job_model.get_savepoint_path())

        # todo 增加最后一次执行的 execution_savepoint_path
        if self.execution_savepoint_path:
            code_list.append('%s %s' % (
            ParagraphProperties.option_items.executionSavepoint.field_name, self.execution_savepoint_path))

        return '\n'.join(code_list)

    def compile_flink_table_config(self):
        code_list = ['%flink', self.flink_job_model.get_flink_table_config()]
        return '\n'.join(code_list)

    def compile_main_task(self):
        """ 生成 job 代码"""
        if self.flink_job_model.task_code_type == CodeParagraph.LanguageType.Sql:
            code_prefix = SQL_CODE_PREFIX_MAP.get(self.flink_job_model.mode)
        else:
            code_prefix = CODE_PREFIX_MAP.get(self.flink_job_model.task_code_type)

        job_properties_config = ParagraphProperties(self.flink_job_model.get_task_properties())

        job_properties_config.o.resumeFromLatestCheckpoint = 'false'

        if self.flink_job_model.mode == self.flink_job_model.Mode.StreamSql:
            job_properties_config.data['type'] = 'update'

        # 添加 任务名称
        job_properties_config.data['jobName'] = self.flink_job_model.name

        # todo 增加最后一次执行的 execution_savepoint_path
        if self.execution_savepoint_path:
            job_properties_config.o.executionSavepoint = self.execution_savepoint_path
        else:
            del job_properties_config.o.executionSavepoint

        job_properties_config.o.resumeFromSavepoint = 'false'
        job_properties_config.o.resumeFromLatestCheckpoint = 'false'
        job_properties_config.o.savepointDir = self.flink_job_model.get_savepoint_path()

        code_prefix = '%s(%s)\n' % (
                code_prefix, ','.join(['%s=%s' % (k, v) for k, v in job_properties_config.data.items() if v]))
        code_list = [code_prefix, '\n-- %s\n' % self.flink_job_model.alias, self.flink_job_model.task_content]
        return '\n'.join(code_list)

    def compile_utfs(self):

        source_text_list = ['%flink']
        # 只支持 scala 的 udf
        source_list: List[CodeParagraph] = [s for s in self.flink_job_model.get_udf() if
                                            s.language == CodeParagraph.LanguageType.Scala]

        source_text_list += [s.text for s in source_list]
        return '\n'.join(source_text_list)

    def get_paragraph_info(self, paragraph_id):
        result = self.zc.get_paragraph_info(self.job_id, paragraph_id)
        return Dict(result)

    def get_flink_job_url(self):
        main_task_paragraph_id = self.get_task_id(TaskTypes.MainTask)
        result = self.get_paragraph_info(main_task_paragraph_id)

        self.last_savepoint_path = result.body.config.savepoint_path or ''
        self.flink_job_url = result.body.runtimeInfos.jobUrl['values'][
                                 0].jobUrl or ''  # http://master:8088/proxy/application_1609290649956_0112/#/job/97742c6511a54f9287581661c30b4dac
        self.flink_job_id = self.flink_job_url.split('#')[-1].split('/')[-1]
        return self.flink_job_url

    def get_last_savepoint_path(self):
        return self.last_savepoint_path

    def get_flink_job_id(self):
        return self.flink_job_id

    def genrate_job_name(self):
        return '/'.join([self.PARENT_PATH, self.flink_job_model.name])

    def get_paragraphs_generator(self):
        return self.get_task_code_generator()

    def genrate_paragraph_data(self, task_type_name, code_text):
        return {"title": task_type_name, "text": code_text}

    def create_job(self):
        paragraphs_list = [self.genrate_paragraph_data(task_type_name, code_generator()) for
                           (task_type_name, code_generator) in
                           self.get_paragraphs_generator().items()]

        result = self.zc.create_note_and_paragraphs(self.genrate_job_name(), paragraphs_list)
        job_id = result['body']
        return job_id

    def delete_note(self):
        try:
            if self.job_id:
                self.zc.delete_note(self.job_id)
        except:
            pass

    def delete_job(self):
        self.delete_note()

    def get_task_id(self, task_name):
        task_info = self.get_task_info(
                task_name)  # {"id":"paragraph_1610440281242_1472177900","status":"READY","progress":"0"}
        task_id = task_info.get('id', None)
        return task_id if task_id else self.status_info.get(task_name, {}).get('id')

    def update_job(self):

        for task_type_name, code_generator in self.get_task_code_generator().items():
            paragraph_id = self.get_task_id(task_type_name)
            paragraph_data = self.genrate_paragraph_data(task_type_name, code_generator())
            result = self.zc.update_paragraph(self.job_id, paragraph_id, **paragraph_data)

    def get_engine_url(self):
        url = '%s/#/notebook/%s' % (FLINK_ZEPPELIN_API_ADDRESS.rstrip('/'), self.flink_job_model.job_id)
        return url

    def get_status_info(self):
        result = self.zc.get_all_paragraphs(self.job_id)
        paragraphs_status_list = result['body']['paragraphs']
        task_name_order_list = self.get_task_name_order_list()
        status_info = OrderedDict(zip(task_name_order_list, paragraphs_status_list))
        return status_info


    def _check_result(self, zc_result):
        return zc_result['status'] == 'OK'

    def run_all_paragraph_sync(self):
        run_info = {}
        self.state.code = EngineStateCode.READY
        for task_type_name, _ in self.get_task_code_generator().items():
            paragraph_id = self.get_task_id(task_type_name)
            if task_type_name == TaskTypes.MainTask:
                # 同步方式启动主任务,会等待任务完成才返回,设置 3 秒超时断开
                self.zc.set_timeout(3);
            try:
                result = self.zc.run_paragraph_sync(task_type_name, self.job_id, paragraph_id)
            except Timeout as e:
                result = {'status': 'OK', 'msg': 'Timeout'}

            run_info[task_type_name] = result.get('body', result)
            if not self._check_result(result):
                self.state.code = EngineStateCode.FAILURE
                break
            task_code = run_info[task_type_name].get('code', '')
            if task_code and task_code != 'SUCCESS':
                self.state.code = EngineStateCode.FAILURE
                self.state.msg = run_info[task_type_name].get('msg', 'ERROR')
                break
            self.state.code = EngineStateCode.SUCCESS
        self.state.data = run_info
        return self.state

    def start(self, execution_savepoint_path=None):
        self.execution_savepoint_path = execution_savepoint_path
        if self.execution_savepoint_path or (
                datetime.datetime.now() - self.flink_job_model.update_datetime).seconds > 5:
            self.save_job()
            time.sleep(0.2)
        self.run_all_paragraph_sync()
        if self.state.code == EngineStateCode.SUCCESS:
            self.wait_status([self.flink_job_model.Status.Running, self.flink_job_model.Status.Finished,
                              self.flink_job_model.Status.Pending, self.flink_job_model.Status.Abort])

        return self.state

    def stop(self, is_force=False):
        self.state.code = EngineStateCode.READY

        main_task_id = self.get_task_id(TaskTypes.MainTask)
        result = self.zc.stop_paragraph(self.job_id, main_task_id)

        if is_force:
            # 杀掉程序 重启启动
            self._wait_stop_status(result)
            result = self.zc.stop_all_paragraphs(self.job_id)
            self._wait_stop_status(result)
            result = self.zc.restart_interpreter(self.job_id, 'flink')

        return self._wait_stop_status(result)

    def _wait_stop_status(self, result):
        self.state.data = result
        self.state.msg = result.get('message', '')
        if self._check_result(result):
            self.wait_status([self.flink_job_model.Status.Abort, self.flink_job_model.Status.Error,
                              self.flink_job_model.Status.Ready, self.flink_job_model.Status.Finished])
            self.state.code = EngineStateCode.SUCCESS
        else:
            self.state.code = EngineStateCode.FAILURE
        return self.state

    def wait_status(self, status_list, timeout=180):
        i = 0
        while 1:
            time.sleep(1)
            if i >= timeout:
                return
            status_info = Dict(self.get_status_info())
            if status_info[TaskTypes.MainTask].status in status_list:
                return
            i += 1
