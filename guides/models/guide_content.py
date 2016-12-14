# -*- coding: utf-8 -*-

from django.db import models


class Guidebody(models.Model):
    title_id = models.ForeignKey(u'guides.GuideTitle',verbose_name=u'文件夹id')
    s_title = models.CharField(u'段落标题', max_length=256, null=True)
    s_body = models.TextField(u'段落正文', null=True)
    image_path = models.CharField(u'图片路径', max_length=256, null=True)
    image_name = models.CharField(u'图片名称', max_length=256, null=True)
    image_msg=models.CharField(u'图片说明',max_length=256,null=True)
    image_location=models.CharField(u'位置',max_length=256,null=True)

    image_explain = models.TextField(u'段落正文', null=True)
    pviews = models.IntegerField(u'阅读量', default=0, null=True)
    collection = models.IntegerField(u'收藏量', default=0, null=True)

    parent = models.IntegerField(u'上一条记录',null=True)

    author_id = models.CharField(u'创建者', max_length=256, null=True)
    write_user = models.CharField(u'更新人', max_length=256, null=True)
    create_date = models.DateTimeField(u'创建时间', auto_now_add=True)
    write_date = models.DateTimeField(u'更新时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文档详细信息'
        verbose_name_plural = '文档标题及详细信息'
        db_table = 'guide_document_body'
