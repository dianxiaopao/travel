# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager


class NewUser(User):
    '''
    这两种方法都可以对user表进行重写
    '''
    show_name = models.CharField(u'显示名称', max_length=255, null=True)
    telephone = models.CharField(u'电话', max_length=255, null=True)
    auth_code = models.CharField(u'验证码', max_length=255, null=True)
    send_date = models.DateTimeField(u'发送时间', null=True)
    objects = UserManager()

# class NewUser(models.Model):
#     user = models.OneToOneField(User)
#     show_name = models.CharField(u'显示名称', max_length=255, null=True)
#     telephone = models.CharField(u'电话', max_length=255, null=True)
