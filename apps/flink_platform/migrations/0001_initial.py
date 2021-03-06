# Generated by Django 2.0.13 on 2021-02-23 14:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import framework.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeParagraph',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('_version', models.IntegerField(default=0, verbose_name='版本')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(db_index=True, help_text='Source 一般为 table name', max_length=100, validators=[django.core.validators.RegexValidator('^[a-z][\\d\\w_]+$', '字母组合,符合^[a-z][\\d\\w_]+$')], verbose_name='段落名')),
                ('alias', models.CharField(blank=True, max_length=100, null=True, verbose_name='段落显示名')),
                ('language', models.CharField(choices=[('sql', 'SQL'), ('python', 'Python'), ('scala', 'Scala')], default='sql', max_length=20, verbose_name='语言类型')),
                ('tag', models.CharField(choices=[('source', 'Flink Source'), ('slink', 'Flink Slink'), ('udf', 'Flink Udf')], max_length=20, verbose_name='段落类型标签')),
                ('text', models.TextField(blank=True, default='', null=True, verbose_name='代码内容')),
                ('group', models.CharField(blank=True, default='', max_length=100, null=True, validators=[django.core.validators.RegexValidator('^[a-z][\\d\\w_]+$', '字母组合,符合^[a-z][\\d\\w_]+$')], verbose_name='组')),
                ('is_share', models.BooleanField(default=True, verbose_name='可共享')),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
            bases=(models.Model, framework.models.SqlModelMixin),
        ),
        migrations.CreateModel(
            name='Connector',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('_version', models.IntegerField(default=0, verbose_name='版本')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[a-z][\\d\\w_]+$', '字母组合,符合^[a-z][\\d\\w_]+$')], verbose_name='名称')),
                ('alias', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='别名')),
                ('type', models.CharField(choices=[('kafka', 'Kafka'), ('kudu', 'Kudu'), ('mysql', 'Mysql'), ('redis', 'Redis'), ('hive', 'Hive'), ('mysql_cdc', 'MysqlCdc')], max_length=10, verbose_name='类型')),
                ('config', framework.models.ObjectDictField(blank=True, default={}, null=True, verbose_name='配置')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, framework.models.SqlModelMixin),
        ),
        migrations.CreateModel(
            name='FlinkJob',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('_version', models.IntegerField(default=0, verbose_name='版本')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[a-z][\\d\\w_]+$', '字母组合,符合^[a-z][\\d\\w_]+$')], verbose_name='任务名')),
                ('alias', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='任务简称')),
                ('status', models.CharField(choices=[('READY', '预备'), ('ABORT', '中止'), ('ERROR', '错误'), ('FINISHED', '完成'), ('PENDING', '启动中'), ('RUNNING', '运行中')], default='READY', max_length=10, verbose_name='任务状态')),
                ('job_id', models.CharField(blank=True, db_index=True, default='', max_length=100, null=True, verbose_name='任务ID')),
                ('flink_job_id', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Flink Job ID')),
                ('flink_job_url', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Flink Job Url')),
                ('mode', models.IntegerField(choices=[(0, '批模式'), (1, '流模式')], default=1, verbose_name='任务模式')),
                ('cron', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='cron 定时执行')),
                ('start_datetime', models.DateTimeField(blank=True, null=True, verbose_name='任务开始执行时间')),
                ('stop_datetime', models.DateTimeField(blank=True, null=True, verbose_name='任务停止执行时间')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='任务备注')),
                ('task_code_type', models.CharField(choices=[('sql', 'SQL'), ('python', 'Python'), ('scala', 'Scala')], default='sql', max_length=20, verbose_name='任务 类型')),
                ('task_content', models.TextField(default='\nset table.dynamic-table-options.enabled=True;\nset table.optimizer.distinct-agg.split.enabled=True;\nset table.exec.mini-batch.enabled=True;\nset table.exec.mini-batch.allow-latency=5s;\nset table.exec.mini-batch.size=5000;\n', verbose_name='任务 内容')),
                ('flink_config', models.TextField(blank=True, default='# https://ci.apache.org/projects/flink/flink-docs-release-1.12/zh/deployment/config.html\n# 设置任务使用的时间属性是eventtime\npipeline.time-characteristic EventTime\n#3 设置checkpoint的时间间隔\nexecution.checkpointing.interval 20000\n# 确保检查点之间的间隔\nexecution.checkpointing.min-pause 60000\n# 设置checkpoint的超时时间\nexecution.checkpointing.timeout 120000\n# 设置任务取消后保留hdfs上的checkpoint文件\nexecution.checkpointing.externalized-checkpoint-retention RETAIN_ON_CANCELLATION\nexecution.savepoint.ignore-unclaimed-state true\n    ', null=True, verbose_name='flink config 配置')),
                ('flink_table_config', models.TextField(blank=True, default='// https://ci.apache.org/projects/flink/flink-docs-stable/zh/dev/table/streaming/query_configuration.html\nimport org.apache.flink.api.common.time.Time\nval env = StreamExecutionEnvironment.getExecutionEnvironment\nval tableEnv = StreamTableEnvironment.create(env)\n// obtain query configuration from TableEnvironment\nval tConfig: TableConfig = tableEnv.getConfig\n// 设置 State TTL\ntConfig.setIdleStateRetentionTime(Time.hours(24), Time.hours(48))\n', null=True, verbose_name='flink table config 配置')),
                ('status_info', framework.models.ObjectDictField(blank=True, default={}, null=True, verbose_name='状态信息')),
                ('task_properties', framework.models.ObjectDictField(blank=True, default={'parallelism': 2, 'runAsOne': True}, null=True, verbose_name='任务属性')),
                ('last_execution_savepoint', models.CharField(blank=True, max_length=2000, null=True, verbose_name='最后 savepoint 路径')),
                ('execution_savepoint_path', models.CharField(blank=True, default='', max_length=2000, null=True, verbose_name='启动 savepoint 路径')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('code_paragraphs', models.ManyToManyField(blank=True, to='flink_platform.CodeParagraph', verbose_name='引用代码段落')),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
            bases=(models.Model, framework.models.SqlModelMixin),
        ),
        migrations.CreateModel(
            name='FlinkJobGroup',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('_version', models.IntegerField(default=0, verbose_name='版本')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(db_index=True, max_length=100, validators=[django.core.validators.RegexValidator('^[a-z][\\d\\w_]+$', '字母组合,符合^[a-z][\\d\\w_]+$')], verbose_name='任务组名')),
                ('alias', models.CharField(max_length=100, verbose_name='任务组描述')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('jobs', models.ManyToManyField(related_name='任务', to='flink_platform.FlinkJob')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='flink_platform.FlinkJobGroup', verbose_name='上级')),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
            bases=(models.Model, framework.models.SqlModelMixin),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('_version', models.IntegerField(default=0, verbose_name='版本')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[a-z][\\d\\w_]+$', '字母组合,符合^[a-z][\\d\\w_]+$')], verbose_name='项目名')),
                ('alias', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='别名')),
                ('appkey', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='秘钥')),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
            bases=(models.Model, framework.models.SqlModelMixin),
        ),
        migrations.CreateModel(
            name='TableColumn',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('_version', models.IntegerField(default=0, verbose_name='版本')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_datetime', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[a-z][\\d\\w_]+$', '字母组合,符合^[a-z][\\d\\w_]+$')], verbose_name='名称')),
                ('alias', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='别名')),
                ('column_type', models.CharField(max_length=10, verbose_name='数据类型')),
                ('column_definition', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='数据类型定义')),
                ('relation', models.ManyToManyField(blank=True, to='flink_platform.CodeParagraph', verbose_name='关联')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, framework.models.SqlModelMixin),
        ),
        migrations.AddField(
            model_name='flinkjob',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flink_platform.Project', verbose_name='所属项目'),
        ),
        migrations.AddField(
            model_name='connector',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flink_platform.Project', verbose_name='所属项目'),
        ),
        migrations.AddField(
            model_name='codeparagraph',
            name='connector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='flink_platform.Connector', verbose_name='所属连接器'),
        ),
    ]
