# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/10/9  22:40'


import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader

#excel导入功能
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)  #返回True才会加载插件

    def block_top_toolbar(self, context, nodes):    #显示自己的html
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context_instance=context))

xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)