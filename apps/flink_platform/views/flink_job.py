# -*- coding: utf-8 -*-
# @Time: 2021-01-14 10:30:06.588324


from drf_yasg.utils import swagger_auto_schema
from celery_task_result.views import TaskIdMapSerializer

from flink_platform.models import FlinkJob, FlinkJobStatusInfoSerializer, FlinkStorageFileListSerializer
from framework.filters import MyFilterBackend, MyFilterSerializer, OrderingFilter
from framework.route import Route
from framework.serializer import BaseModelSerializer, EditParams, IdSerializer, IdsSerializer, PaginationSerializer, \
    RelationModelIdField, s
from framework.translation import _
from framework.utils import DATETIMEFORMAT
from framework.views import action_get, action_post, CurdViewSet, render_to_response as rt
from ..tasks import restart_flink_job, start_flink_job, stop_flink_job


class FlinkJobSerializer(BaseModelSerializer):
    # https://www.django-rest-framework.org/api-guide/serializers/
    # https://www.django-rest-framework.org/api-guide/relations/
    # code_paragraphs = s.PrimaryKeyRelatedField(many=True,label=_("引用代码段落"),queryset=FlinkJob.code_paragraphs.field.related_model.objects.all() )
    # author = s.RelatedField(label=_("作者"),queryset=FlinkJob.author.field.related_model.objects.all())
    author_alias = s.CharField(required=False, read_only=True)
    project_alias = s.CharField(required=False, read_only=True)
    status_alias = s.CharField(source='get_status_display', required=False, read_only=True)
    mode_alias = s.CharField(source='get_mode_display', required=False, read_only=True)
    task_code_type_alias = s.CharField(source='get_task_code_type_display', required=False, read_only=True)
    status_info = FlinkJobStatusInfoSerializer(label=('任务状态信息'), required=False, read_only=True)

    source_list = RelationModelIdField(source='get_source', required=False, read_only=True)
    slink_list = RelationModelIdField(source='get_slink', required=False, read_only=True)
    udf_list = RelationModelIdField(source='get_udf', required=False, read_only=True)

    start_datetime = s.DateTimeField(label=_('创建时间'), format=DATETIMEFORMAT, required=False, read_only=False,
                                     allow_null=True)
    stop_datetime = s.DateTimeField(label=_('更新时间'), format=DATETIMEFORMAT, required=False, read_only=True,
                                    allow_null=True)

    class Meta:
        model = FlinkJob
        fields = ['id', 'project', 'author_alias', 'project_alias', 'author', 'name', 'alias', 'status', 'job_id',
                  'flink_job_id', 'flink_job_url', 'mode', 'cron',
                  'start_datetime', 'stop_datetime', 'remark', 'code_paragraphs', 'task_code_type', 'task_content',
                  'flink_config', 'flink_table_config', 'status_info', 'task_properties', 'last_execution_savepoint',
                  'create_datetime', 'update_datetime', 'status_alias', 'mode_alias',
                  'task_code_type_alias', 'execution_savepoint_path', 'source_list', 'slink_list',
                  'udf_list'] or '__all__'
        # exclude = ['session_key']
        read_only_fields = ['create_datetime', 'update_datetime', 'start_datetime', 'stop_datetime', 'status_info',
                            'status', 'flink_job_id', 'flink_job_url']
        # extra_kwargs = {'password': {'write_only': True}}


class ListFlinkJobRspSerializer(PaginationSerializer):
    results = FlinkJobSerializer(many=True)


@Route('flink_platform/flink_job')
class FlinkJobSet(CurdViewSet):
    filter_backends = (MyFilterBackend, OrderingFilter)

    serializer_class = FlinkJobSerializer
    # 可条件过滤的字段
    filter_fields = ['id', 'project', 'author', 'name', 'alias', 'status', 'job_id', 'flink_job_id', 'flink_job_url',
                     'mode',
                     'start_datetime', 'stop_datetime', 'code_paragraphs', 'task_code_type', 'last_execution_savepoint',
                     'create_datetime', 'update_datetime']
    # 可排序的字段
    ordering_fields = ['id', 'project', 'author', 'name', 'alias', 'status', 'job_id', 'create_datetime',
                       'update_datetime']
    # 可以查询字段
    queryset_fields = ['id', 'project', 'author', 'name', 'alias', 'status', 'flink_job_id', 'flink_job_url', 'mode',
                       'job_id',
                       'cron', 'start_datetime', 'stop_datetime', 'task_code_type', 'execution_savepoint_path',
                       'last_execution_savepoint', 'create_datetime', 'update_datetime']

    model = FlinkJob

    def get_queryset(self):
        return FlinkJob.objects.all().prefetch_related(*['code_paragraphs']).select_related().only(
                *FlinkJobSet.queryset_fields)

    @swagger_auto_schema(query_serializer=MyFilterSerializer, responses=ListFlinkJobRspSerializer)
    def list(self, request):
        """FlinkJob 列表"""

        return rt("flink_platform/flink_job/list.html", super(FlinkJobSet, self).list(request))

    @swagger_auto_schema(query_serializer=EditParams, responses=FlinkJobSerializer)
    def edit(self, request):
        """FlinkJob 编辑"""

        model_instance: FlinkJob = self.get_model_instance(EditParams)
        if self.is_copy:
            model_instance.id = 0
            model_instance.job_id = ''
            model_instance.flink_job_id = ''
            model_instance.flink_job_url = ''
            model_instance.last_execution_savepoint = ''
            model_instance.execution_savepoint_path = ''
        serializer = self.get_serializer(instance=model_instance)

        return rt("flink_platform/flink_job/edit.html", serializer.data)

    @swagger_auto_schema(query_serializer=IdSerializer, request_body=FlinkJobSerializer, responses=FlinkJobSerializer)
    def save(self, request):
        """FlinkJob 保存"""
        flink_job_model: FlinkJob = self.get_model_instance(IdSerializer)
        flink_job_model.status = FlinkJob.Status.Ready
        ser, msg = self.save_instance(request, flink_job_model)
        flink_job_model = ser.instance
        flink_job_model.sync_engine_job()

        return self.response(ser, msg=msg)

    @swagger_auto_schema(request_body=IdsSerializer, responses=IdsSerializer)
    def delete(self, request):
        """FlinkJob 删除"""
        params = IdsSerializer(request.data).params_data

        if params.id:
            ids = params.id
            for model in self.get_queryset().filter(id__in=ids):
                model.delete()
            return self.response(data=params)
        return self.response(params, msg=_('ids empty'))

    class FlinkJobActionParams(IdsSerializer):
        force = s.BooleanField(label=_('是否强制执行'), required=False)
        use_last_savepoint = s.BooleanField(label=_('是否 使用最后一次 Savepoint Path'), required=False, default=True)

    @swagger_auto_schema(request_body=IdsSerializer, responses=TaskIdMapSerializer)
    @action_post()
    def start(self, request):
        """异步启动 Job"""
        parmas = self.FlinkJobActionParams(request.data).params_data
        ser = TaskIdMapSerializer()

        if parmas.id:
            for id in parmas.id:
                task_state = start_flink_job.delay(id, parmas.use_last_savepoint)
                ser.o.idmap[id] = task_state.id

        return self.response(ser)

    @swagger_auto_schema(request_body=IdsSerializer, responses=TaskIdMapSerializer)
    @action_post()
    def stop(self, request):
        """异步停止 Job"""
        parmas = self.FlinkJobActionParams(request.data).params_data
        ser = TaskIdMapSerializer()
        if parmas.id:
            for id in parmas.id:
                task_state = stop_flink_job.delay(id, parmas.force)
                ser.o.idmap[id] = task_state.id

        return self.response(ser)

    @swagger_auto_schema(request_body=IdsSerializer, responses=TaskIdMapSerializer)
    @action_post()
    def restart(self, request):
        """异步重启 Job"""
        parmas = self.FlinkJobActionParams(request.data).params_data
        ser = TaskIdMapSerializer()
        if parmas.id:
            for id in parmas.id:
                task_state = restart_flink_job.delay(id, parmas.force, parmas.use_last_savepoint)

                ser.o.idmap[id] = task_state.id

        return self.response(ser)

    @swagger_auto_schema(query_serializer=IdSerializer, responses=FlinkJobSerializer(fields=queryset_fields))
    @action_get()
    def status_info(self, request):
        """获取 Flink Job 任务信息 """
        flink_job_model = self.get_model_instance(queryset=self.get_queryset())
        ser = FlinkJobSerializer(many=True)
        if flink_job_model.id:
            flink_job_model.update_status_info()
            ser = self.get_serializer(flink_job_model, fields=self.queryset_fields + ['status_info'])
        return self.response(ser)

    @swagger_auto_schema(query_serializer=IdSerializer, responses=FlinkStorageFileListSerializer)
    @action_get()
    def storage_file_list(self, request):
        """获取 Flink Job  savepoint 保存目录信息  """
        flink_job_model: FlinkJob = self.get_model_instance(queryset=self.get_queryset())
        ser = FlinkStorageFileListSerializer()
        if flink_job_model.id:
            ser = FlinkStorageFileListSerializer({'points':flink_job_model.get_storage_file_list()})
        return self.response(ser)

# @swagger_auto_schema(methods=['post'], request_body=FlinkJobSerializer, responses=FlinkJobSerializer)
# @action(['post'])
# def foo_action(self, request):
#     return Response(FlinkJobSerializer().data)
