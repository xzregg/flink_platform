# coding=utf-8
# 启动守护进程


# supervisord 管理设置 http://supervisord.org/configuration.html
INET_HTTP_SERVER_LISTEN = '0.0.0.0:19001'
INET_HTTP_SERVER_USERNAME = 'admin'
INET_HTTP_SERVER_PASSWORD ='P@ssword'


DAEMON_SERVICE_MAP = {
        "statistic"  : {"cmd": "python -u manage.py StatisticCron -c", "remark": "统计后台服务"},
        #"ldap"       : {"cmd": "python3 -u manage.py ldap_server ", "remark": "ldap 服务"},
}
