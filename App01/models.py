# coding=utf-8

from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from DjangoUeditor.models import UEditorField


# Create your models here.
class LofterModel(models.Model):
    title = models.CharField(max_length=30, default="", verbose_name=u"文章标题")
    timestamp = models.DateTimeField(default=datetime.now, verbose_name=u"发表时间")
    image = models.ImageField(null=True, blank=True, default="courses/2017/09/p1.jpg", upload_to="courses/%Y/%m",
                              verbose_name=u"封面图", max_length=100)
    # content = models.TextField(verbose_name=u"文章内容")
    content = UEditorField(u'内容详情', width=750, height=300, imagePath="ueditor/", filePath="ueditor/",
                           upload_settings={"imageMaxSize": 1204000}, default="")
    author_id = models.IntegerField(verbose_name=u"作者ID", blank=True, null=True)
    fav_click = models.IntegerField(default=0, verbose_name=u"点赞数")

    def __unicode__(self):
        return self.title

    def get_author_name(self):
        from Users.models import UserInfo
        person = UserInfo.objects.get(id=self.author_id)
        return person.username

    get_author_name.short_description = u"作者名字"

    class Meta:
        verbose_name = u"发表文章"
        verbose_name_plural = verbose_name
