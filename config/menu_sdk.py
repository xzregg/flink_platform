#格式: 索引 菜单名 url(只是全选也需要占位) 类型(0 不显示菜单,记录日志,1 不显示菜单,不记录日志 ,2 显示菜单,记录日志)
from django.utils.translation import ugettext_lazy as _
from framework.route import reverse_view
from myadmin.models.menu import MenuConfig as _m
from .menu_system import MenuList

MenuList = [

_m('8',_('聚合 SDK')),
	_m('8.0',_('我的游戏项目'),' /projects/list'),
		_m('8.0.0',_('游戏项目_编辑'),'/projects/edit',0, 0),
		_m('8.0.1',_('游戏项目_保存'),'/projects/save',0, 0),
		_m('8.0.2',_('游戏项目_删除'),'/projects/remove',0, 0),
	_m('8.0', _('发行计划'), ' /analysis/query/view/发行计划'),

	_m('8.1',_('游戏项目版本'),'/projects_version/list',0,0),
		_m('8.1.0',_('游戏项目版本_编辑'),'/projects_version/edit',0, 0),
		_m('8.1.1',_('游戏项目版本_保存'),'/projects_version/save',0, 0),
		_m('8.1.2',_('游戏项目版本_删除'),'/projects_version/remove',0, 0),
		_m('8.1.3', _('游戏项目版本SDK'), '/query/view/游戏项目版本SDK', 0, 0),
			_m('8.1.3.0', _('游戏版本SDK_编辑'), '/projects_version_sdk/edit', 0, 0),
			_m('8.1.3.1', _('游戏版本SDK_保存'), '/projects_version_sdk/save', 0, 0),
			_m('8.1.3.2', _('增加SDK接入'), '/projects_version_sdk/edit', 0, 0),
			_m('8.1.3.3', _('取消SDK接入'), '/projects_version_sdk/remove', 0, 0),
			_m('8.1.3.4', _('更新SDK配置'), '/sdk/game/push_config', 0, 0),

	_m('8.3',_('SDK列表'),' /sdk_center/sdk/list',is_show=1),
		_m('8.3.0',_('SDK_编辑'),'/sdk_center/sdk/edit',0, 0),
		_m('8.3.1',_('SDK_保存'),'/sdk_center/sdk/save',0, 0),
		_m('8.3.2',_('SDK_删除'),'/sdk_center/sdk/delete',0, 0),
	_m('8.4',_('SDK版本列表'),'/sdk_center/sdk_version/list',is_show=0),
		_m('8.4.0',_('SDK版本_编辑'),'/sdk_center/sdk_version/edit',0, 0),
		_m('8.4.1',_('SDK版本_保存'),'/sdk_center/sdk_version/save',0, 0),
		_m('8.4.2',_('SDK版本_删除'),'/sdk_center/sdk_version/delete',0, 0),
	_m('8.5', _('渠道')),
		_m('8.5.0', _('渠道公司'), reverse_view('sdk_center.channel.channel_company_list')),
			_m('8.5.0.1', _('渠道公司_编辑'), reverse_view('sdk_center.channel.channel_company_edit'), 0, 0),
			_m('8.5.0.2', _('渠道公司_保存'), reverse_view('sdk_center.channel.channel_company_save'), 0, 0),
			_m('8.5.0.3', _('渠道公司_删除'), reverse_view('sdk_center.channel.channel_company_remove'), 0, 0),
		_m('8.5.1', _('渠道管理'), reverse_view('sdk_center.channel.channel_list')),
			_m('8.5.1.1', _('二级渠道_编辑'), reverse_view('sdk_center.channel.channel_edit'), 0, 0),
			_m('8.5.1.2', _('二级渠道_保存'), reverse_view('sdk_center.channel.channel_save'), 0, 0),
			_m('8.5.1.3', _('二级渠道_删除'), reverse_view('sdk_center.channel.channel_remove'), 0, 0),
			_m('8.5.1.5', _('一级渠道_编辑'), reverse_view('sdk_center.channel.agent_edit'), 0, 0),
			_m('8.5.1.6', _('一级渠道_保存'), reverse_view('sdk_center.channel.agent_save'), 0, 0),
			_m('8.5.1.7', _('一级渠道_删除'), reverse_view('sdk_center.channel.agent_remove'), 0, 0),
	_m('8.9', _('服管理'), reverse_view('sdk_center.server.server_list'),is_show=1),
	_m('8.8', _('服分区管理'), reverse_view('sdk_center.group.group_list'),is_show=1),


]+MenuList
