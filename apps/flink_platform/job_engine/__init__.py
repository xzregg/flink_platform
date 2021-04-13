# -*- coding: utf-8 -*-
# @Time    : 2021-01-07 15:28
# @Author  : xzr
# @File    : __init__
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :
import json
import logging

import requests
from framework.utils import ObjectDict, OrderedDict, trace_msg
from framework.utils.cache import CacheAttribute
from framework.utils.myenum import Enum
from furl import furl


class EngineStateCode(Enum):
    SUCCESS = 0, 'SUCCESS'
    READY = 1, 'READY'
    STARTED = 2, 'STARTED'

    FAILURE = 3, 'FAILURE'

    REVOKED = 4, 'REVOKED'

    REJECTED = 5, 'REJECTED'

    RETRY = 6, 'RETRY'
    IGNORED = 7, 'IGNORED'


class StateStructure(ObjectDict):
    code = EngineStateCode.READY
    msg = ''
    data = {}


class BaseFlinkJobEngine(object):

    def __init__(self, flink_job_model):
        from ..models.flink_job import FlinkJob
        self.flink_job_model: FlinkJob = flink_job_model
        self.state = StateStructure()
        self.flink_job_id = ''
        self.flink_job_url = ''
        self.job_id = self.flink_job_model.job_id
        self.execution_savepoint_path = self.flink_job_model.execution_savepoint_path

    def compile_source(self):
        raise Exception("rewrite the method")

    def compile_slink(self):
        raise Exception("rewrite the method")

    def compile_flink_config(self):
        raise Exception("rewrite the method")

    def compile_flink_table_config(self):
        raise Exception("rewrite the method")

    def compile_utfs(self):
        raise Exception("rewrite the method")

    def get_flink_job_url(self):
        raise Exception("rewrite the method")

    def get_flink_job_id(self):
        raise Exception("rewrite the method")

    def get_last_savepoint_path(self):
        raise Exception("rewrite the method")

    def get_savepoint_path_list(self):
        raise Exception("rewrite the method")

    def get_engine_url(self):
        raise Exception("rewrite the method")

    @CacheAttribute
    def status_info(self):
        return self.get_status_info()

    def get_task_info(self, task_name):
        return self.flink_job_model.status_info.get(task_name, {}) or self.status_info.get(task_name, {})

    def get_task_name_order_list(self):
        return self.get_task_code_generator().keys()

    def get_task_code_generator(self) -> OrderedDict:
        from ..models.flink_job import TaskTypes
        task_code_generator_map = OrderedDict()
        task_code_generator_map[TaskTypes.Config] = self.compile_flink_config

        task_code_generator_map[TaskTypes.Source] = self.compile_source
        task_code_generator_map[TaskTypes.Slink] = self.compile_slink

        task_code_generator_map[TaskTypes.Udf] = self.compile_utfs
        task_code_generator_map[TaskTypes.TableConfig] = self.compile_flink_table_config
        task_code_generator_map[TaskTypes.MainTask] = self.compile_main_task

        return task_code_generator_map

    def update_main_task_status(self):
        from ..models.flink_job import FlinkJob, TaskTypes
        ret = {'status': FlinkJob.Status.Error}
        if self.flink_job_id and self.flink_job_url and self.flink_job_model.status != self.flink_job_model.Status.Abort:
            try:
                base_furl = furl(self.flink_job_url)
                base_furl.fragment = ''
                base_furl.path.add('jobs').add(self.flink_job_id)
                rsp = requests.get(base_furl.url, timeout=3)
                # flink job status https://ci.apache.org/projects/flink/flink-docs-release-1.12/zh/ops/rest_api.html
                ret = rsp.json()
                ret['status'] = ret['state']
                if ret['status'] != FlinkJob.Status.Finished:
                    self.status_info[TaskTypes.MainTask].update(ret)
            except json.decoder.JSONDecodeError as e:
                pass
            except KeyError as e:
                pass
            except Exception as e:
                logging.error('%s get main task statue error %s' % (self.flink_job_model.name, trace_msg()))
        return self.status_info

    def delete_job(self):
        raise Exception("rewrite the method")

    def save_job(self) -> str:
        """
        保存 Flink Job
        :return: job_id
        """
        if self.job_id:
            self.update_job()
            return ''
        else:
            self.job_id = self.create_job()
            return self.job_id

    def update_job(self):
        raise Exception("rewrite the method")

    def create_job(self) -> str:
        raise Exception("rewrite the method")

    def get_status_info(self):
        raise Exception("rewrite the method")

    def start(self, execution_savepoint_path):
        self.state.msg = "rewrite start method"
        return self.state

    def stop(self, is_force=False):
        self.state.msg = "rewrite stop method"
        return self.state

    def restart(self, is_force=False):
        self.state.msg = "rewrite restart method"
        return self.state
