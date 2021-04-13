# -*- coding: utf-8 -*-

import datetime
import logging
from typing import List

from celery_task.models import AssociatedTaskResult, ReturnResultTask
from config.celery_app import app, Task
from .models.flink_job import FlinkJob


@app.task(bind=True, base=ReturnResultTask)
def stop_flink_job(self: Task, flink_job_model_id, is_force):
    a_task_result = AssociatedTaskResult.create_for_task(self, flink_job_model_id)

    flink_job_model: FlinkJob = FlinkJob.objects.filter(id=flink_job_model_id).first()

    return flink_job_model.stop(is_force)


@app.task(bind=True, base=ReturnResultTask)
def start_flink_job(self: Task, flink_job_model_id, use_last_savepoint=True):
    a_task_result = AssociatedTaskResult.create_for_task(self, flink_job_model_id, )

    flink_job_model: FlinkJob = FlinkJob.objects.filter(id=flink_job_model_id).first()
    result = flink_job_model.start(use_last_savepoint)
    return result


@app.task(bind=True, base=ReturnResultTask)
def restart_flink_job(self: Task, flink_job_model_id, is_force, use_last_savepoint=True):
    a_task_result = AssociatedTaskResult.create_for_task(self, flink_job_model_id, )

    flink_job_model: FlinkJob = FlinkJob.objects.filter(id=flink_job_model_id).first()

    statue = flink_job_model.restart(is_force, use_last_savepoint)
    return statue


@app.task(bind=True, ignore_result=True)
def cron_refresh_flink_job_info(self: Task):
    flink_jobs: List[FlinkJob] = FlinkJob.objects.exclude(
            status__in=[FlinkJob.Status.Finished, FlinkJob.Status.Abort, FlinkJob.Status.Error]).exclude(job_id='').defer(
        'code_paragraphs',
        'flink_table_config',
        'task_properties')
    for flink_job_mode in flink_jobs:
        flink_job_mode.update_status_info()
        logging.info("%s update_status_info  [%s]" % (flink_job_mode.name, flink_job_mode.status))


@app.task(ignore_result=True)
def cron_live(arg):
    logging.info("%s flink_job is live " % datetime.datetime.now())


app.conf.beat_schedule = {
        'tell-me-live-every-10-seconds'         : {
                'task'    : 'flink_platform.tasks.cron_live',
                'schedule': 10,
                'args'    : (16,)
        },
        'refresh_flink_job_info-every-2-seconds': {
                'task'    : 'flink_platform.tasks.cron_refresh_flink_job_info',
                'schedule': 2,  # crontab('*','*','*','*','*'),
                'args'    : ()
        },
}

app.conf.task_routes.update({'flink_platform.tasks.cron_*': {'queue': 'cron'}})
