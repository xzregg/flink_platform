# -*- coding: utf-8 -*-
# @Time: 2021-02-25 16:40:43.675715


from drf_yasg.utils import swagger_auto_schema
from framework.filters import MyFilterBackend, OrderingFilter, MyFilterSerializer
from framework.translation import _
from framework.route import Route
from framework.serializer import s,BaseModelSerializer, EditParams, IdSerializer, IdsSerializer, ParamsSerializer, PaginationSerializer
from framework.views import CurdViewSet, ListPageNumberPagination, Response,action,Request
from framework.views import render_to_response as rt
from flink_platform.models import Connector


class ConnectorSerializer(BaseModelSerializer):
    # https://www.django-rest-framework.org/api-guide/serializers/
    # https://www.django-rest-framework.org/api-guide/relations/
    #project = s.RelatedField(label=_("所属项目"),queryset=Connector.project.field.related_model.objects.all())
    type_alias = s.CharField(source='get_type_display',required=False, read_only=True)
    project_alias = s.CharField(required=False, read_only=True)
    class Meta:
        model = Connector
        fields =  ['id', 'name', 'alias', 'project', 'project_alias','type', 'config', 'create_datetime', 'update_datetime', 'type_alias'] or '__all__'
        #exclude = ['session_key']
        read_only_fields = ['create_datetime', 'update_datetime']
        #extra_kwargs = {'password': {'write_only': True}}


class ListConnectorRspSerializer(PaginationSerializer):
    results = ConnectorSerializer(many=True)

@Route('flink_platform/connector')
class ConnectorSet(CurdViewSet):
    filter_backends = (MyFilterBackend,OrderingFilter)

    serializer_class = ConnectorSerializer
    # 可条件过滤的字段
    filter_fields =  ['id', 'name', 'alias', 'project', 'type', 'create_datetime', 'update_datetime']
    # 可排序的字段
    ordering_fields = ['id', 'name', 'alias', 'project', 'type', 'create_datetime', 'update_datetime']
    # 可以查询字段
    queryset_fields = ['id', 'name', 'alias', 'project', 'type',  'create_datetime', 'update_datetime']

    model = Connector

    def get_queryset(self):
        return Connector.objects.all().prefetch_related(*[]).select_related(*['project']).only(*ConnectorSet.queryset_fields)

    @swagger_auto_schema(query_serializer=MyFilterSerializer,responses=ListConnectorRspSerializer)
    def list(self, request):
        """Flink 连接器 列表"""
        return rt("flink_platform/connector/list.html",super().list(request))

    @swagger_auto_schema(query_serializer=EditParams, responses=ConnectorSerializer)
    def edit(self, request):
        """Flink 连接器 编辑"""
        return rt("flink_platform/connector/edit.html",super().edit(request))

    @swagger_auto_schema(query_serializer=IdSerializer,request_body=ConnectorSerializer, responses=ConnectorSerializer)
    def save(self, request):
        """Flink 连接器 保存"""
        return super().save(request)

    @swagger_auto_schema(request_body=IdsSerializer, responses=IdsSerializer)
    def delete(self, request):
        """Flink 连接器 删除"""
        return super().delete(request)


    # @swagger_auto_schema(methods=['post'], request_body=ConnectorSerializer, responses=ConnectorSerializer)
    # @action(['post'])
    # def foo_action(self, request):
    #     return Response(ConnectorSerializer().data)