# coding=utf-8
"""MyLofter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from django.contrib import admin
from MyLofter.settings import MEDIA_ROOT
from django.views.static import serve
from App01.views import IndexView, AddFavView, PerBlogView, RefreshView, AddCommentsView, UserBlogView ,UserIndexView
from django.views.decorators.cache import cache_page

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    # url(r'^$', IndexView.as_view(), name="index"),
    url(r'^$', cache_page(60*60)(IndexView.as_view()), name="index"),

    url(r'^blog/(?P<blog_id>\d+)/$', PerBlogView.as_view(), name="per_blog"),

    url(r'^uid/(?P<uid>\d+)/$', UserIndexView.as_view(), name="user_index"),
    url(r'^uid/(?P<uid>\d+)/blog/(?P<bid>\d+)/$', UserBlogView.as_view(), name="user_blog"),

    url(r'add_comment/$', AddCommentsView.as_view(), name="add_comment"),

    url(r'add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 配置上传图片文件的路径
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),

    url(r'^user/', include('Users.urls', namespace='users')),

    # 添加验证码路径
    url(r'^captcha/', include('captcha.urls')),

    # 刷新验证码
    url(r'refresh-captcha/$', RefreshView.as_view(), name="refresh-captcha"),
]
