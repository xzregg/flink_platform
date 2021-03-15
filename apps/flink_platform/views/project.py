# -*- coding: utf-8 -*-
# @Time: 2021-02-03 18:57:19.139044


from drf_yasg.utils import swagger_auto_schema
from framework.filters import MyFilterBackend, OrderingFilter, MyFilterSerializer
from framework.translation import _
from framework.route import Route
from framework.serializer import s,BaseModelSerializer, EditParams, IdSerializer, IdsSerializer, ParamsSerializer, PaginationSerializer
from framework.views import CurdViewSet, ListPageNumberPagination, Response,action,Request
from framework.views import render_to_response as rt,notcheck
from flink_platform.models import Project


class ProjectSerializer(BaseModelSerializer):
    # https://www.django-rest-framework.org/api-guide/serializers/
    # https://www.django-rest-framework.org/api-guide/relations/

    class Meta:
        model = Project
        fields =  ['id', 'name', 'alias', 'appkey', 'create_datetime', 'update_datetime'] or '__all__'
        #exclude = ['session_key']
        read_only_fields = ['create_datetime', 'update_datetime']
        #extra_kwargs = {'password': {'write_only': True}}


class ListProjectRspSerializer(PaginationSerializer):
    results = ProjectSerializer(many=True)

@Route('flink_platform/project')
class ProjectSet(CurdViewSet):
    filter_backends = (MyFilterBackend,OrderingFilter)

    serializer_class = ProjectSerializer
    # 可条件过滤的字段
    filter_fields =  ['id', 'name', 'alias', 'appkey', 'create_datetime', 'update_datetime']
    # 可排序的字段
    ordering_fields = ['id', 'name', 'alias', 'appkey', 'create_datetime', 'update_datetime']
    # 可以查询字段
    queryset_fields = ['id', 'name', 'alias', 'appkey', 'create_datetime', 'update_datetime']

    model = Project

    def get_queryset(self):
        return Project.objects.all().prefetch_related(*[]).select_related(*[]).only(*ProjectSet.queryset_fields)

    @swagger_auto_schema(query_serializer=MyFilterSerializer,responses=ListProjectRspSerializer)
    def list(self, request):
        """项目 列表"""
        return rt("flink_platform/project/list.html",super().list(request))

    @swagger_auto_schema(query_serializer=EditParams, responses=ProjectSerializer)
    def edit(self, request):
        """项目 编辑"""
        return rt("flink_platform/project/edit.html",super().edit(request))

    @swagger_auto_schema(query_serializer=IdSerializer,request_body=ProjectSerializer, responses=ProjectSerializer)
    def save(self, request):
        """项目 保存"""
        return super().save(request)

    @swagger_auto_schema(request_body=IdsSerializer, responses=IdsSerializer)
    def delete(self, request):
        """项目 删除"""
        return super().delete(request)


    # @swagger_auto_schema(methods=['post'], request_body=ProjectSerializer, responses=ProjectSerializer)
    # @action(['post'])
    # def foo_action(self, request):
    #     return Response(ProjectSerializer().data)