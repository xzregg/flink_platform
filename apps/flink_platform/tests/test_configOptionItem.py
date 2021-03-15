# -*- coding: utf-8 -*-
# @Time    : 2021-01-07 17:22
# @Author  : xzr
# @File    : test_configOptionItem
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    :

from __future__ import absolute_import
from framework.serializer import ConfigOptionSerializer, s
from framework.tests import BaseTestCase


class TestConfigOptionItem(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_a(self):
        from framework.enums import BoolEnum
        from flink_platform.models.flink_job import ParagraphProperties
        p = ParagraphProperties()
        del p.o.executionSavepoint
        self.assertIs(ParagraphProperties().o.refreshInterval, p.data.refreshInterval)
        self.assertIs(p.o.executionSavepoint, None)
