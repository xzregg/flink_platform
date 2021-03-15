# Register your models here.

from framework.translation import _
from myadmin.models import ModelResource, Resource
from .models.project import Project


class FlinkProjectModelResource(ModelResource):
    label = _('Flink 项目')
    name = 'flink_project'
    model_class = Project
    template_context = {}
    template = ModelResource.default_template

Resource.register(FlinkProjectModelResource())
