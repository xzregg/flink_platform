# -*- coding: utf-8 -*-
# @Time : 2020-06-08 11:48
# @Author : xzr
# @File : role.py
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc : 定义基本角色


from framework.translation import _
from myadmin.models.role import Role

RoleList = [
        ('root', _('超级管理员'), Role.RoleType.USER, ''),
        ('analysis', _('分析用户'), Role.RoleType.USER, ''),
        ('yunying', _('项目运营'), Role.RoleType.USER, ''),
        ('channel_user', _('渠道用户'), Role.RoleType.USER, ''),
        ('jishu', _('项目技术'), Role.RoleType.USER, ''),
        ('ceshi', _('项目测试'), Role.RoleType.USER, ''),
        ('cehua', _('项目策划'), Role.RoleType.USER, ''),
        ('tech', _('公共技术组'), Role.RoleType.GROUP, ''),
        ('sdk', _('sdk组'), Role.RoleType.GROUP, 'tech'),
        ('sdk_server', _('服务端组'), Role.RoleType.GROUP, 'sdk'),
        ('sdk_client', _('客户端组'), Role.RoleType.GROUP, 'sdk'),
]
