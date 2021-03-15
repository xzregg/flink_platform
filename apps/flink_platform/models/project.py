# -*- coding: utf-8 -*-
# @Time    : 2021-01-25 18:17
# @Author  : xzr
# @File    : project
# @Software: PyCharm
# @Contact : 
# @Desc    : 


from django.db import models
from django.utils.translation import ugettext_lazy as _

from framework.models import BaseModel
from framework.validators import LetterValidator


class Project(BaseModel):
    """项目"""
    name = models.CharField(_('项目名'), max_length=100, null=False, blank=False, validators=[LetterValidator],
                            unique=True)

    alias = models.CharField(_('别名'), max_length=100, default='', null=True, blank=True)

    appkey = models.CharField(_('秘钥'), max_length=100, default='', null=True, blank=True)