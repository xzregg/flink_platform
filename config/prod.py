# -*- coding: utf-8 -*-
# @Time    : 2019-08-28 16:20
# @Author  : xzr
# @File    : __init__
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 正式环境 settings 基本设置


# SECURITY WARNING: don't run with debug turned on in production!

import logging
import os
DEBUG = False

from settings import BASE_DIR

logging.info('This env is production,DEBUG = False')
logging.info('BASE_DIR: %s' % BASE_DIR)

DATABASES = {
        'default': {
                # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or
                # 'oracle'.
                'ENGINE'  : 'django.db.backends.mysql',
                # Or path to database file if using sqlite3.
                'NAME'    : 'flink_platform',
                'USER'    : 'root',  # Not used with sqlite3
                'PASSWORD': 'youai123',  # youai123                  # Not used with sqlite3.youai123
                # 211.100.100.141#118.26.226.187',#'115.238.101.83',
                # # Set to empty string for localhost. Not used with sqlite3
                'HOST'    : 'cdh_mysql',
                # Set to empty string for default. Not used with sqlite3.
                'PORT'    : '3306',
                # 'CONN_MAX_AGE':None,
                'OPTIONS' : {'isolation_level': None}
        },
        'read'   : {
                # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or
                # 'oracle'.
                'ENGINE'  : 'django.db.backends.mysql',
                # Or path to database file if using sqlite3.
                'NAME'    : 'flink_platform',
                'USER'    : 'root',  # Not used with sqlite3.
                'PASSWORD': 'youai123',  # youai123                  # Not used with sqlite3.youai123
                # 211.100.100.141#118.26.226.187',#'115.238.101.83',
                # # Set to empty string for localhost. Not used with sqlite3
                'HOST'    : 'cdh_mysql',
                # Set to empty string for default. Not used with sqlite3.
                'PORT'    : '3306',
                'OPTIONS' : {'isolation_level': None}
        },
        'write'  : {
                # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or
                # 'oracle'.
                'ENGINE'  : 'django.db.backends.mysql',
                # Or path to database file if using sqlite3.
                'NAME'    : 'flink_platform',
                'USER'    : 'root',  # Not used with sqlite3.
                'PASSWORD': 'youai123',  # youai123                  # Not used with sqlite3.youai123
                # 211.100.100.141#118.26.226.187',#'115.238.101.83',
                # # Set to empty string for localhost. Not used with sqlite3
                'HOST'    : 'cdh_mysql',
                # Set to empty string for default. Not used with sqlite3.
                'PORT'    : '3306',
                'OPTIONS' : {'isolation_level': None}

        },
        'ldap'   : {
                'ENGINE'  : 'ldapdb.backends.ldap',
                'NAME'    : 'ldap://127.0.0.1:389',
                'USER'    : 'cn=admin,dc=example,dc=com',
                'PASSWORD': 'ldap123',
        }
}
DATABASES['read'] = DATABASES['default']
DATABASES['write'] = DATABASES['default']
DATABASES['db'] = DATABASES['default']