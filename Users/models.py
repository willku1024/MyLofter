# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.
from App01.models import LofterModel

class UserInfo(AbstractUser):
    # gender = models.CharField(choices=(("male", u"男"), ("female", u"女")), default="", max_length=6)
    # image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(default="", max_length=20, verbose_name="散列码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证类型", choices=(("register", u"注册"), ("forget", u"忘记密码")), max_length=10)
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.email, self.code)



class Comments(models.Model):
    '''文章评论'''
    comment_user = models.ForeignKey(UserInfo, verbose_name=u"用户",blank=True,null=True)
    essay = models.ForeignKey(LofterModel, verbose_name=u"文章")
    comments = models.CharField(max_length=100, verbose_name=u"评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    anonymous_user = models.CharField(max_length=40, verbose_name=u"匿名",blank=True,null=True)

    class Meta:
        verbose_name = u"文章评论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.comments

