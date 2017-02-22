# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from base.models.new_user import NewUser
import json

try:
    from django.apps import apps as models
except ImportError:  # django < 1.7
    from django.db import models




def index(request):
    return render(request, 'index.html')


def get_login(request):
    '''
    获取登陆页
    :param request:
    :return:
    '''
    return render(request, 'login.html')


def alogin(request, *args, **kwargs):
    '''
    登陆页面
    :param request:
    :param args:
    :param kwargs:
    :return:
    '''
    username = request.POST['username']
    password = request.POST['password']
    try:
        User.objects.get(username=username)
    except:
        return render(request, 'login.html', {'error_msg': u"账户不存在"})
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/mycenter/note/create/')
        # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            return render(request, 'login.html',{"error_msg":u'账户被禁用'})
    else:
        return render(request, 'login.html',{"error_msg":u'密码错误'})


def accounts_alogin(request):
    return render(request, 'login.html')

