# -*- coding: utf-8 -*-
# @Time    : 2021-03-17 13:20
# @Author  : xzr
# @File    : api
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 不能在 import settings 前导入

from drf_yasg import openapi


API_INFO = openapi.Info(
        title="Flink Platfrom API",
        default_version='v1',
        description="Platfrom description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License")
)
