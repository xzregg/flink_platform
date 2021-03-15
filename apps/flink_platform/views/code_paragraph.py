# -*- coding: utf-8 -*-
# @Time: 2021-01-13 16:27:15.650639


from typing import List

from addict import Dict
from drf_yasg.utils import swagger_auto_schema

from flink_platform.models import CodeParagraph
from framework.filters import MyFilterBackend, MyFilterSerializer, OrderingFilter
from framework.route import Route
from framework.serializer import BaseModelSerializer, DataSerializer, EditParams, IdSerializer, IdsSerializer, \
    PaginationSerializer, ParamsSerializer, RecursiveField, s
from framework.translation import _
from framework.views import action_get, CurdViewSet, render_to_response as rt
from framework.utils import ObjectDict


class CodeParagraphSerializer(BaseModelSerializer):
    # https://www.django-rest-framework.org/api-guide/serializers/
    # https://www.django-rest-framework.org/api-guide/relations/
    language_alias = s.CharField(source='get_language_display', required=False, read_only=True)
    tag_alias = s.CharField(source='get_tag_display', required=False, read_only=True)
    project_alias = s.CharField(required=False, read_only=True)
    class Meta:
        model = CodeParagraph
        fields = ['id', 'name', 'alias','project','project_alias', 'language', 'tag', 'text', 'create_datetime', 'update_datetime',
                  'language_alias', 'tag_alias', 'connector', 'group', 'is_share','table_schema'] or '__all__'
        # exclude = ['session_key']
        read_only_fields = ['create_datetime', 'update_datetime','table_schema']
        # write_only_fields = ['text']
    # extra_kwargs = {'text': {'write_only': True}}


class ListCodeParagraphRspSerializer(PaginationSerializer):
    results = CodeParagraphSerializer(many=True)


class CodeParagraphsTreeItemSer(DataSerializer):
    title = s.CharField(label=_('标题'))
    key = s.CharField(label=_('值'))
    children = RecursiveField(label=_('子项目'))


class CodeParagraphsTreeListSer(DataSerializer):
    source = CodeParagraphsTreeItemSer(required=False, many=True)
    slink = CodeParagraphsTreeItemSer(required=False, many=True)
    udf = CodeParagraphsTreeItemSer(required=False, many=True)


@Route('flink_platform/code_paragraph')
class CodeParagraphSet(CurdViewSet):
    """代码段"""
    filter_backends = (MyFilterBackend, OrderingFilter)

    serializer_class = CodeParagraphSerializer
    # 可条件过滤的字段
    filter_fields = ['id', 'connector', 'name', 'alias', 'project','language', 'tag', 'text', 'create_datetime',
                     'update_datetime', 'is_share']
    # 可排序的字段
    ordering_fields = ['id', 'connector', 'name', 'alias', 'project','language', 'tag', 'create_datetime', 'update_datetime']
    # 可查询的字段
    queryset_fields = ['id', 'name', 'alias', 'language','project', 'tag', 'create_datetime', 'update_datetime', 'connector',
                       'is_share','group','table_schema']
    model = CodeParagraph

    def get_queryset(self):
        return CodeParagraph.objects.all().prefetch_related(*['project','connector']).select_related(*[]).only(
                *CodeParagraphSet.queryset_fields)

    @swagger_auto_schema(query_serializer=MyFilterSerializer, responses=ListCodeParagraphRspSerializer)
    def list(self, request):
        """Flink 代码段 列表"""

        return rt("flink_platform/code_paragraph/list.html",
                  super().list(request))

    @swagger_auto_schema(query_serializer=EditParams, responses=CodeParagraphSerializer)
    def edit(self, request):
        """Flink 代码段 编辑"""
        model_instance:CodeParagraph = self.get_model_instance(EditParams)
        if not model_instance.id:
            model_instance.tag = request.query_params.get('tag',model_instance.tag)
        serializer = self.get_serializer(instance=model_instance)
        return rt("flink_platform/code_paragraph/edit.html",serializer.data)

    @swagger_auto_schema(query_serializer=IdSerializer, request_body=CodeParagraphSerializer,
                         responses=CodeParagraphSerializer)
    def save(self, request):
        """Flink 代码段 保存"""
        return super().save(request)

    @swagger_auto_schema(request_body=IdsSerializer, responses=IdsSerializer)
    def delete(self, request):
        return super().delete(request)

    class ParagraphsTreeParmas(ParamsSerializer):
        is_project_private = s.BooleanField(label=_('是否项目独有'), required=False, default=False)

    @swagger_auto_schema(query_serializer=ParagraphsTreeParmas, responses=CodeParagraphsTreeListSer)
    @action_get()
    def code_paragraphs_tree(self, request):
        """树信息"""
        params = self.ParagraphsTreeParmas(request.query_params).params_data
        query_set = self.get_queryset()
        if params.is_project_private:
            query_set = self.get_queryset().filter(is_share=False)

        model_list: List[CodeParagraph] = self.filter_queryset(query_set)
        code_paragraphs_tree_map = Dict()

        for model in model_list:
            tag_name = model.tag
            connector_name = model.connector.type if model.connector else ''
            group_name = model.group or ''

            code_paragraphs_tree_map[tag_name][connector_name].setdefault(group_name, [])
            parent_list = code_paragraphs_tree_map[tag_name][connector_name][group_name]

            child_item = ObjectDict(title=model.name, key=model.id, alias=model.alias,table_schema=model.table_schema)
            parent_list.append(child_item)

        return self.response(code_paragraphs_tree_map)

    # @swagger_auto_schema(methods=['post'], request_body=CodeParagraphSerializer, responses=CodeParagraphSerializer)
    # @action(['post'])
    # def foo_action(self, request):
    #     return Response(CodeParagraphSerializer().data)
