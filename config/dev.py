# -*- coding: utf-8 -*-
# @Time    : 2019-08-28 16:20
# @Author  : xzr
# @File    : __init__
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 开发环境 settings 基本设置


# SECURITY WARNING: don't run with debug turned on in production!

import logging
import os
import sys

from . import logging_config

DEBUG = True

from django.conf import settings

# session引擎设置
# SESSION_ENGINE='django.contrib.sessions.backends.cache'
# SESSION_COOKIE_AGE = 60 * 30  # 30分钟
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览器，则COOKIE失效
# CACHES = {
#         'default': {
#                 'BACKEND' : 'django.core.cache.backends.filebased.FileBasedCache',
#                 'LOCATION': os.path.join(BASE_DIR, 'django_cache'),
#         }
# }

STATICFILES_DIRS = [os.path.join(settings.BASE_DIR, 'static')]
STATIC_ROOT = None
_DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME'  : os.path.join(settings.BASE_DIR, 'db.sqlite3'),
                'TEST'  : {
                        'NAME': os.path.join(settings.BASE_DIR, 'test.db.sqlite3')

                }
        },

}

DATABASES = {
        'default': {

                'ENGINE'  : 'django.db.backends.mysql',

                'NAME'    : 'djmyadmin',
                'USER'    : 'root',
                'PASSWORD': '123456',

                'HOST'    : '10.19.200.185',

                'PORT'    : '3306',

                'OPTIONS' : {'isolation_level': None},

        }

}

DATABASES['card'] = DATABASES['default'].copy()

if 'test' in sys.argv:
    # 使用内存数据库加速测试
    DATABASES = {
            'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME'  : ':memory'
            }
    }


DATABASES['read'] = DATABASES['default'].copy()
DATABASES['write'] = DATABASES['default'].copy()

PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
]
# vINSTALLED_APPS += ['django_extensions']

# INSTALLED_APPS += ['debug_toolbar']
INTERNAL_IPS = [
        '*',
        '127.0.0.1'
]

# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': '',
}
logging.warning('This env is dev,DEBUG = True')
logging.warning('BASE_DIR: %s' % settings.BASE_DIR)

# 日志打印 sql
logging_config.LOGGING['loggers']['1django.db.backends'] = {
        'handlers' : ['console'],
        'propagate': False,
        'level'    : 'DEBUG',
}
