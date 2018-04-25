# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/9/12  15:38'


from .models import  EmailVerifyRecord, Comments
from App01.models import  LofterModel
import xadmin


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_export = ['xls', 'xml', 'json']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class CommentsAdmin(object):
    list_display = ['comment_user', 'essay', 'comments', 'add_time','anonymous_user']
    search_fields = ['comment_user', 'essay', 'comments','anonymous_user']  
    list_export = ['xls', 'xml', 'json']
    list_filter = ['comment_user', 'essay', 'comments', 'add_time','anonymous_user']
    
    def queryset(self):
        qs = super(CommentsAdmin, self).queryset()
        if self.user.is_superuser:
            return qs
        else:
            my_essay = LofterModel.objects.filter(author_id=self.user.id).defer('title', 'timestamp', 'content', 'fav_click', 'author_id','image').values_list('id', flat=True)
            my_essay = list(my_essay)
            return qs.filter(essay_id__in=my_essay)

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Comments, CommentsAdmin)


