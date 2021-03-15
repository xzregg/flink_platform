#格式: 索引 菜单名 url(只是全选也需要占位) 类型(0 不显示菜单,记录日志,1 不显示菜单,不记录日志 ,2 显示菜单,记录日志)
from django.utils.translation import ugettext_lazy as _

from myadmin.models.menu import MenuConfig as _m
from .menu_system import MenuList

MenuList = [
_m('6',_('都爱刷广告')),
	_m('6.1', _('App 管理'), '/advertisement_brush_roboot/brush_app/list',is_log=0,is_show=1),
		_m('6.1.1', _('App 编辑'), '/advertisement_brush_roboot/brush_app/edit', is_log=0, is_show=0),
		_m('6.1.2', _('App 保存'), '/advertisement_brush_roboot/brush_app/save', is_log=1, is_show=0),
		_m('6.1.3', _('App 删除'), '/advertisement_brush_roboot/brush_app/delete', is_log=1, is_show=0),
	_m('6.2', _('激活码 管理'), '/advertisement_brush_roboot/activation_code/list', is_log=0, is_show=1),
		_m('6.2.1', _('激活码 编辑'), '/advertisement_brush_roboot/activation_code/edit', is_log=0, is_show=0),
		_m('6.2.2', _('激活码 保存'), '/advertisement_brush_roboot/activation_code/save', is_log=1, is_show=0),
		_m('6.2.3', _('激活码 删除'), '/advertisement_brush_roboot/activation_code/delete', is_log=1, is_show=0),
	_m('6.3', _('续费记录'), '/advertisement_brush_roboot/renewal_record/list', is_log=0, is_show=1),
		_m('6.3.1', _('续费记录 编辑'), '/advertisement_brush_roboot/renewal_record/edit', is_log=0, is_show=0),
		_m('6.3.2', _('续费记录 保存'), '/advertisement_brush_roboot/renewal_record/save', is_log=1, is_show=0),
		_m('6.3.3', _('续费记录 删除'), '/advertisement_brush_roboot/renewal_record/delete', is_log=1, is_show=0),

]+MenuList
