# -*- coding: utf-8 -*-
# @Time    : 2021-03-08 10:43
# @Author  : xzr
# @File    : test_pyflink
# @Software: PyCharm
# @Contact : xzregg@gmail.com
# @Desc    : 

from pyflink.table import EnvironmentSettings, StreamTableEnvironment


env_settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
table_env = StreamTableEnvironment.create(environment_settings=env_settings)

table_env.execute_sql("""
    CREATE TABLE datagen (
        id INT,
        data STRING
    ) WITH (
        'connector' = 'datagen',
        'fields.id.kind' = 'sequence',
        'fields.id.start' = '1',
        'fields.id.end' = '10'
    )
""")

table_env.execute_sql("""
    CREATE TABLE print (
        id INT,
        data STRING
    ) WITH (
        'connector' = 'print'
    )
""")

source_table = table_env.from_path("datagen")
source_table = table_env.sql_query("SELECT * FROM datagen")
result_table = source_table.select(source_table.id + 1, source_table.data)
result_table.execute_insert("print").wait()
# 只有 insert 类才能指定 jobName
#table_env.sql_update('insert into print SELECT * FROM datagen')
#table_env.execute('as;dkl')


table_env.get_config().get_configuration().set_string("restart-strategy", "fixed-delay")
table_env.get_config().get_configuration().set_string("restart-strategy.fixed-delay.attempts", "3")

table_env.get_config().get_configuration().set_string("restart-strategy.fixed-delay.delay", "20s")

table_env.get_config().get_configuration().set_string("execution.checkpointing.mode", "EXACTLY_ONCE")
table_env.get_config().get_configuration().set_string("execution.checkpointing.interval", "2min")
table_env.get_config().get_configuration().set_string("execution.checkpointing.min-pause", "1min")
table_env.get_config().get_configuration().set_string("execution.checkpointing.timeout", "10min")
table_env.get_config().get_configuration().set_string("execution.checkpointing.externalized-checkpoint-retention", "RETAIN_ON_CANCELLATION")
table_env.get_config().get_configuration().set_string("state.backend", "rocksdb")


table_env.get_config().get_configuration().set_string("state.checkpoints.dir", "file:///tmp/checkpoints/")
table_env.get_config().get_configuration().set_string("state.savepoints.dir", "file:///tmp/savepoints/")
table_env.get_config().get_configuration().set_string("state.backend.local-recovery", "true")
table_env.get_config().get_configuration().set_string("parallelism.default", "3")

table_env.get_config().get_configuration().set_string('execution.savepoint.ignore-unclaimed-state','false')

table_env.get_config().get_configuration().set_string('execution.savepoint.path','file:///tmp/checkpoints/')

table = table_env.from_elements([(1, 'Hi'), (2, 'Hello')], ['id', 'data'])
table_env.create_temporary_view('source_table', table)

# create Table API table from catalog
new_table = table_env.from_path('source_table')
new_table.to_pandas()





