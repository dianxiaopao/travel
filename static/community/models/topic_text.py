# -*- coding: utf-8 -*-
from django.db import models
import mycenter.models.img_material


class TopicText(models.Model):
    name = models.CharField(u'主题', max_length=256)
    text = models.TextField(u'内容', null=True)

    forum_sort = models.ForeignKey('community.ForumSort', null=True, related_name='+', verbose_name='分类名称')
    u_public = models.BooleanField(u'是否公开', default=True)
    a_public = models.BooleanField(u'是否公开', default=True)
    priority = models.IntegerField(u'优先级', default=0, null=True)
    pviews = models.IntegerField(u'阅读量', default=0, null=True)
    collection = models.IntegerField(u'收藏量', default=0, null=True)

    create_user = models.ForeignKey('auth.User', blank=True, null=True, related_name='+', verbose_name='创建人')
    create_date = models.DateTimeField(u'创建时间', auto_now_add=True)
    write_user = models.ForeignKey('auth.User', blank=True, null=True, related_name='+', verbose_name='更新人')
    write_date = models.DateTimeField(u'更新时间', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'论坛分类'
        verbose_name_plural = u'论坛分类'
        db_table = 'comm_topic_text'
