
[group:gsdk_login]
programs=sdk_login

[program:sdk_login]
process_name= %(program_name)s_40%(process_num)02d
command=/usr/bin/env python -u /data/www/sdk_center/sdk_validator_server/server.py --port=40%(process_num)02d
directory=/data/www/sdk_center/sdk_validator_server/
autorestart=true
redirect_stderr=true
stdout_logfile=/data/www/sdk_center/sdk_validator_server/login.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=50
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
loglevel = warn
numprocs = 8
numprocs_start = 1


[group:gsdk_pay]
programs=sdk_pay

[program:sdk_pay]
process_name= %(program_name)s_50%(process_num)02d
command=/usr/bin/env python -u /data/www/sdk_center/sdk_validator_server/server.py --port=50%(process_num)02d
directory=/data/www/sdk_center/sdk_validator_server/
autorestart=true
redirect_stderr=true
stdout_logfile=/data/www/sdk_center/sdk_validator_server/pay.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=50
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
loglevel = warn
numprocs = 8
numprocs_start = 1

[group:gsdk_statistic]
programs=sdk_statistic

[program:sdk_statistic]
process_name= %(program_name)s_30%(process_num)02d
command=/usr/bin/env python -u /data/www/sdk_center/manage.py StatisticServer --port=30%(process_num)02d
directory=/data/www/sdk_center/
autorestart=true
redirect_stderr=true
stdout_logfile=/data/www/sdk_center/sdk_statistic.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=50
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
loglevel = warn
numprocs = 8
numprocs_start = 1

