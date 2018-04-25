# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/10/14  22:42'


from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class LoginRequiredMiddleware:
    def process_request(self, request):
        if not request.user.is_authenticated():
            has_str = request.path_info.find('admin')
            if has_str != -1:
                return HttpResponseRedirect(reverse('users:login'))
