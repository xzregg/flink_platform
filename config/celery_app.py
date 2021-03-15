# -*- coding: utf-8 -*-
# @Time    : 2019-09-02 17:57
# @Author  : xzr
# @File    : celery_app
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery, Task
from celery.result import AsyncResult

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('celery_app')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

from django.conf import settings
#settings.DEBUG = False
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# 设置任务路由 启动 celery 进程 用 -Q myadmin
# app.conf.task_routes = {'myadmin.tasks.*': {'queue': 'myadmin'}}
app.conf.task_routes = {}
