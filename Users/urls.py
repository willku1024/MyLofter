# _*_ coding: utf-8 _*_
__author__ = 'x_jwei@qq.com'
__date__ = '2017/9/28  18:52'

from django.conf.urls import url
from .views import MusicView, SongView, LoginView, RegisterView, ForgetPwdView, ActiveUserView, ResetView, LogoutView , ManageView

urlpatterns = [

    url(r'^music/$', MusicView.as_view(), name="163_music"),

    url(r'^song/(?P<list_id>.*)$', SongView.as_view(), name="song_music"),

    url(r'^login/$', LoginView.as_view(), name="login"),

    url(r'^logout/$', LogoutView.as_view(), name="logout"),

    url(r'^manage/$', ManageView.as_view(), name="manage"),

    url(r'^register/$', RegisterView.as_view(), name="register"),

    url(r'^forget/$', ForgetPwdView.as_view(), name="forget"),

    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),

    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),

]
