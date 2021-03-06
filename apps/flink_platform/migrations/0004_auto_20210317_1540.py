# Generated by Django 2.0.13 on 2021-03-17 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flink_platform', '0003_codeparagraph_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flinkjob',
            name='flink_config',
            field=models.TextField(blank=True, default='#全局任务 https://ci.apache.org/projects/flink/flink-docs-release-1.12/zh/deployment/config.html\nrestart-strategy fixed-delay\nrestart-strategy.fixed-delay.attempts 3\nrestart-strategy.fixed-delay.delay 20s\nstate.checkpoints.num-retained 3 \nexecution.checkpointing.tolerable-failed-checkpoints 3\n# 设置任务使用的时间属性是eventtime\npipeline.time-characteristic EventTime\n# 设置checkpoint的时间间隔\nexecution.checkpointing.interval 5min\n# 确保检查点之间的间隔\nexecution.checkpointing.min-pause 1min\n# 设置checkpoint的超时时间\nexecution.checkpointing.timeout 10min\n# 设置任务取消后保留hdfs上的checkpoint文件\nexecution.checkpointing.externalized-checkpoint-retention RETAIN_ON_CANCELLATION\nexecution.savepoint.ignore-unclaimed-state true\n    ', null=True, verbose_name='flink config 配置'),
        ),
        migrations.AlterField(
            model_name='flinkjob',
            name='flink_table_config',
            field=models.TextField(blank=True, default='// 额外执行代码 变量参考 http://zeppelin.apache.org/docs/0.9.0/interpreter/flink.html#paragraph-local-properties\n// https://ci.apache.org/projects/flink/flink-docs-stable/zh/dev/table/streaming/query_configuration.html\n\nimport org.apache.flink.api.common.time.Time\nval env = senv\nval tableEnv = stenv\nval tConfig: TableConfig = tableEnv.getConfig\nval configuration = tConfig.getConfiguration()\n// 设置 State TTL\n//tConfig.setIdleStateRetentionTime(Time.hours(24), Time.hours(48))\n//configuration.setString("execution.checkpointing.interval", "2min")\n//configuration.setString("execution.checkpointing.min-pause", "1min")\n//configuration.setString("execution.checkpointing.timeout", "10min")\n', null=True, verbose_name='flink table config 配置'),
        ),
        migrations.AlterField(
            model_name='flinkjob',
            name='task_content',
            field=models.TextField(default='\n-- 任务优化参数 https://ci.apache.org/projects/flink/flink-docs-release-1.12/dev/table/config.html\nset table.dynamic-table-options.enabled=True;\nset table.optimizer.distinct-agg.split.enabled=True;\nset table.exec.mini-batch.enabled=True;\nset table.exec.mini-batch.allow-latency=5s;\nset table.exec.mini-batch.size=5000;\nset table.exec.state.ttl=2d;\n', verbose_name='任务 内容'),
        ),
    ]
