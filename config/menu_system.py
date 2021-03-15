#格式: 索引 菜单名 url(只是全选也需要占位) 类型(0 不显示菜单,记录日志,1 不显示菜单,不记录日志 ,2 显示菜单,记录日志)
from django.utils.translation import ugettext_lazy as _
from framework.route import reverse_view
from myadmin.models.menu import MenuConfig as _m

MenuList = [

_m('17',_('系统管理')),
	_m('17.2',_('用户设置'),'/myadmin/user/list'),
		_m('17.2.1',_('用户_添加'),'/myadmin/user/edit',0, 0),
		_m('17.2.2',_('用户_编辑'),'/myadmin/user/delete',0, 0),
			_m('17.2.2.1',_('修改用户密码'),name='change_user_password',is_show=0,is_log=1),
		_m('17.2.3',_('用户_保存'),'/myadmin/user/save',is_show=0,is_log=1),
	_m('17.3', _('用户资料'), '/myadmin/user_info/list', is_log=0, is_show=1),
		_m('17.3.5', _('用户资料_编辑'), '/myadmin/user_info/edit', 0, 0),
		_m('17.3.6', _('用户资料_保存'), '/myadmin/user_info/save', 0, 0),
	_m('17.4',_('操作日志'),'/myadmin/operate_log/list',0,1),
	_m('17.5', _('菜单管理'), '/myadmin/menu/list'),
		_m('17.5.1', _('菜单_编辑'), '/myadmin/menu/edit', 0, 0),
		_m('17.5.2', _('菜单_删除'), '/myadmin/menu/delete', 0, 0),
		_m('17.5.2', _('菜单_保存'), '/myadmin/menu/save', 0, 0),

	_m('17.6',_('日志类管理'),'/log_def/log_define/list'),
		_m('17.6.1',_('日志_编辑'),'/log_def/log_define/edit',0, 0),
		_m('17.6.2',_('日志_删除'),'/log_def/log_define/save',0, 0),
		_m('17.6.3',_('日志_保存'),'/log_def/log_define/delete',0, 0),
	_m('17.7',_('字典管理'),'/log_def/dict_define/list'),
		_m('17.7.1',_('字典_编辑'),'/log_def/dict_define/edit',0, 0),
		_m('17.7.2',_('字典_保存'),'/log_def/dict_define/save',0, 0),
		_m('17.7.3',_('字典_删除'),'/log_def/dict_define/delete',0, 0),

	_m('17.8',_('查询管理'),' /analysis/query/list'),
		_m('17.8.1',_('查询_编辑'),'/analysis/query/edit',0, 0),
		_m('17.8.2',_('查询_删除'),'/analysis/query/remove',0, 0),
		_m('17.8.3',_('查询_保存'),'/analysis/query/save',0, 0),
		_m('17.8.4',_('查询_导出'),'/analysis/query/view?is_export=true',0, 0),
		_m('17.8.5',_('清除缓存'),'/analysis/query/clear/cache',0, 0),
		_m('17.8.6',_('查询权限'),'/analysis/query/view',0,0),

	_m('17.9',_('统计管理'),' /analysis/statistic/list'),
		_m('17.9.1',_('统计_编辑'),'/analysis/statistic/edit',0, 0),
		_m('17.9.2',_('统计_保存'),'/analysis/statistic/save',0, 0),
		_m('17.9.3',_('统计_删除'),'/analysis/statistic/remove',0, 0),
		_m('17.9.4',_('统计_执行'),'/analysis/statistic/execute',0, 0),

	_m('17.10',_('同步模型'),'/sync/backstage/list'),
		_m('17.10.1', _('同步模型_编辑'), '/sync/backstage/edit', 0, 0),
		_m('17.10.2', _('同步模型_保存'), '/sync/backstage/save', 0, 0),
		_m('17.10.3', _('同步模型_删除'), '/sync/backstage/remove', 0, 0),
		_m('17.10.4', _('同步模型_推送'), '/sync/backstage/push', 0, 0),

_m('18', _('SVN 管理'), reverse_view('svn_admin.svn_path.list'),is_show=1,is_log=0),
	_m('18.1', _('SVN 路径_编辑'), reverse_view('svn_admin.svn_path.edit'), 0, 0),
	_m('18.2', _('SVN 路径_保存'), reverse_view('svn_admin.svn_path.save'), 0, 0),
	_m('18.3', _('SVN 路径_删除'), reverse_view('svn_admin.svn_path.delete'), 0, 0),
	_m('18.3', _('SVN db 文件预览'), reverse_view('svn_admin.svn_path.preview_db_files'), 0, 0),

_m('29',_('用户权限'),'',0,0),
	_m('29.1',_('主页'), '/index', 1, 0),
	_m('29.2',_('首页'),'/home', 1,0),
	_m('29.3',_('修改自己密码'),'/myadmin/user/change_password',0, 0),
	_m('29.4',_('字典_接口'),'/log/dict/interface',1, 0),
	_m('29.5',_('用户自定义菜单'),'/system/menu/user_menu_list',1, 0),
	_m('29.6',_('消息列表'),'system/message/message_list',1, 0),
	_m('29.6',_('任务查询'),'celery_task_result/query',is_show=0,is_log= 0)
]
