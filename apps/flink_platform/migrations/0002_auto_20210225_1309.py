# Generated by Django 2.0.13 on 2021-02-25 13:09

import django.core.validators
from django.db import migrations, models
import framework.models


class Migration(migrations.Migration):

    dependencies = [
        ('flink_platform', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='codeparagraph',
            name='table_schema',
            field=framework.models.ObjectDictField(default={}, verbose_name='包含的表格信息'),
        ),
        migrations.AlterField(
            model_name='codeparagraph',
            name='alias',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='段落显示名'),
        ),
        migrations.AlterField(
            model_name='codeparagraph',
            name='group',
            field=models.CharField(blank=True, default='', max_length=100, validators=[django.core.validators.RegexValidator('^[a-z][\\d\\w_]+$', '字母组合,符合^[a-z][\\d\\w_]+$')], verbose_name='组'),
        ),
        migrations.AlterField(
            model_name='codeparagraph',
            name='text',
            field=models.TextField(blank=True, default='', verbose_name='代码内容'),
        ),
        migrations.AlterField(
            model_name='connector',
            name='alias',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='别名'),
        ),
        migrations.AlterField(
            model_name='flinkjob',
            name='task_properties',
            field=framework.models.ObjectDictField(blank=True, default={'execution.savepoint.path': '', 'maxParallelism': 32768, 'parallelism': 2, 'refreshInterval': 5000, 'resumeFromLatestCheckpoint': False, 'resumeFromSavepoint': False, 'runAsOne': False, 'savepointDir': ''}, null=True, verbose_name='任务属性'),
        ),
        migrations.AlterField(
            model_name='tablecolumn',
            name='alias',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='别名'),
        ),
    ]
