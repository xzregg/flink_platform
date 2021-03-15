# -*- coding: utf-8 -*-




import settings

FLINK_SAVEPOINT_PATH_BACKEND_ADDRESS = "http://master:50070"

FLINK_SAVEPOINT_ROOT_PATH = 'hdfs:///user/flink_zeppelin/'

FLINK_JOB_ENGINE = 'job_engine.zeppelin.FlinkJobEngine'

FLINK_ZEPPELIN_API_ADDRESS = 'http://master:18080/'

FLINK_ZEPPELIN_API_USER = ''

FLINK_ZEPPELIN_API_PASSWORD = ''

locals().update(settings.__dict__)
