# -*- coding: utf-8 -*-
from django.db import models


class GuideTitle(models.Model):
    uuid=models.CharField('uuid',max_length=256)
    title = models.CharField(u'标题', max_length=256, null=True,default=u'未命名草稿')
    abstract = models.TextField(u'摘要', null=True)
    type = models.CharField(u'文章类型', max_length=256, null=True)
    source = models.CharField(u'文章来源', max_length=256, null=True)
    pviews = models.IntegerField(u'阅读量', default=0, null=True)
    collection = models.IntegerField(u'收藏量', default=0, null=True)

    u_public=models.BooleanField(u'是否公开',default=False)
    a_public=models.BooleanField(u'是否公开',default=True)

    priority=models.IntegerField(u'优先级',default=0)

    author_id = models.CharField(u'创建者', max_length=256, null=True)
    write_user = models.CharField(u'更新人', max_length=256, null=True)
    create_date = models.DateTimeField(u'创建时间', auto_now_add=True)
    write_date = models.DateTimeField(u'更新时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'文档详细信息'
        verbose_name_plural = u'文档标题及详细信息'
        db_table = 'guide_document_title'
