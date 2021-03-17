# http://supervisord.org/configuration.html
# https://docs.gunicorn.org/en/latest/settings.html

[program:uwsgi]
process_name=uwsgi
command=uwsgi --ini config/uwsgi.ini
directory=%(here)s/../../
priority=1
autorestart=false
redirect_stderr=true
stdout_logfile=logs/uwsgi.log
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stderr_logfile=logs/uwsgi.error.log
stderr_logfile_maxbytes=100MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
stdout_events_enabled=false
loglevel = warn
stopsignal=QUIT
killasgroup=true
environment=PYTHONUNBUFFERED="TRUE"


