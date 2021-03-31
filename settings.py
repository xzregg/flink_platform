
from __future__ import absolute_import

import os
import sys

DEBUG = True
SECRET_KEY = '--x!2w(*_e(h0y&gw%n%%3bjo2&!5q*j7h!ijv#x_w=^)spmdr'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APPS = ['flink_platform','djmyframework']
APPS_ROOT = os.path.join(BASE_DIR, 'apps')

from djmyframework.settings import *
TITLE = 'Flink 管理平台'

INSTALLED_APPS.remove('ldap_account')

FLINK_SAVEPOINT_PATH_BACKEND_ADDRESS = "http://h1:50070"
FLINK_ZEPPELIN_API_ADDRESS = 'http://h29:18080/'

PROJECT_ROOT = BASE_DIR

