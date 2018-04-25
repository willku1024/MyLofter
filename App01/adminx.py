# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/9/12  15:38'

import xadmin
from xadmin import views
from djcelery import admin
from .models import LofterModel
from Users.models import UserInfo


class BaseSetting(object):
    enable_themes = True
    use_bootswacth = True


class GlobalSettings(object):
    site_title = "后台管理系统"
    site_footer = "coderr.cn"
    menu_style = "accordion"


class LofterModelAdmin(object):
    list_display = ['title', 'timestamp', 'content', 'fav_click', 'author_id']
    search_fields = ['title', 'content', 'fav_click', 'author_id']
    list_export = ['xls', 'xml', 'json']
    list_filter = ['title', 'timestamp', 'content', 'fav_click', 'author_id']
    style_fields = {"content": "ueditor"}
    readonly_fields = ['author_id', 'fav_click']

    def save_models(self):
        obj = self.new_obj
        if obj.author_id:
            obj.save()
        else:
            obj.author_id = self.user.id
            obj.save()

    def queryset(self):
        qs = super(LofterModelAdmin, self).queryset()
        if self.user.is_superuser:
            return qs
        else:
            return qs.filter(author_id=self.user.id)


xadmin.site.register(LofterModel, LofterModelAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
