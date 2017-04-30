# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User
from base.models.new_user import NewUser
from django.http import HttpResponse, Http404
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from utils import send_email_on_code
import base.views.base_views as base_view
import traceback, json, smtplib, datetime, random

get_user_data = base_view.UserView().get_user_data

# Create your views here.

try:
    from django.apps import apps as models
except ImportError:  # django < 1.7
    from django.db import models


class Home(object):
    def __init__(self):
        self.user_valid = False

    def home(self, request, *args, **kwargs):
        username = kwargs.get("username")
        try:
            user_obj = User.objects.get(username=username)
        except:
            return render(request, 'login.html')

        return render(request, 'home.html')

    def settings(self, request):
        user = request.user
        if not user:
            return render(request, 'login.html')
        else:
            def get_single_user_data(user):
                if hasattr(user, "newuser"):
                    telephone = user.newuser.telephone if user.newuser.telephone else ""
                    show_name = user.newuser.show_name if user.newuser.show_name else ""
                else:
                    telephone = ''
                    show_name = ''
                if user.email:
                    deft_valid = "email"
                elif telephone:
                    deft_valid = "telephone"
                else:
                    deft_valid = False
                data = {
                    "email": user.email,
                    "username": user.username,
                    "id": user.id,
                    "telephone": telephone,
                    "show_name": show_name,
                    "deft_valid": deft_valid
                }
                return data

            data = get_single_user_data(user)

        return render(request, "setting.html", context=data)

    def get_email_code(self, request):

        result = {}
        try:
            email = request.GET.get("email")
            user = request.user
            to_addr = email.encode("utf-8")
            try:
                new_obj = User.objects.get(username=user.username)
            except:
                raise Exception("没有%s这个用户" % user.username)

            auth_code = int(random.uniform(1000, 9999))
            if hasattr(new_obj, "newuser"):
                new_obj.newuser.auth_code = auth_code
                new_obj.newuser.send_date = timezone.now()
                new_obj.newuser.save()
                new_obj.save()
            else:
                user_dict = {
                    "username": new_obj.username,
                    "password": new_obj.password,
                    "last_login": new_obj.last_login,
                    "is_superuser": new_obj.is_superuser,
                    "email": new_obj.email,
                    "first_name": new_obj.first_name,
                    "last_name": new_obj.last_name,
                    "send_date": timezone.now(),
                    "auth_code": auth_code
                }
                u_obj = NewUser.objects.update_or_create(id=new_obj.id, defaults=user_dict)
                u_obj[0].save()

            msg_text = u"本次验证码为：%s" % str(auth_code)
            # 发邮件
            result["result"] = send_email_on_code(msg_text, to_addr)

        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(result))

    def save_new_email(self, request):
        result = {}
        try:
            auth_code = request.GET.get("auth_code")
            new_email = request.GET.get("email")
            username = request.user.username
            u_obj = NewUser.objects.filter(username=username)
            if not u_obj:
                result["result"] = "用户名不正确"
            else:
                u_obj = u_obj[0]
                if u_obj.auth_code == auth_code:
                    u_obj.email = new_email
                    u_obj.save()
                    result["result"] = True
                else:
                    result["result"] = "验证码不正确"
        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(result))

    def send_valid_code(self, request):
        result = {}
        try:
            valid = request.GET.get("valid")
            if valid == "email":
                try:
                    new_obj = User.objects.get(username=request.user.username)
                except:
                    raise Exception("没有查询到当前用户！")
                email = new_obj.email.encode("utf-8")
                auth_code = int(random.uniform(1000, 9999))

                user_dict = {
                    "username": new_obj.username,
                    "password": new_obj.password,
                    "last_login": new_obj.last_login,
                    "is_superuser": new_obj.is_superuser,
                    "email": new_obj.email,
                    "first_name": new_obj.first_name,
                    "last_name": new_obj.last_name,
                    "auth_code": auth_code,
                    "send_date": timezone.now()

                }
                u_obj = NewUser.objects.update_or_create(id=new_obj.id, defaults=user_dict)
                u_obj[0].save()

                msg_text = u"本次验证码为：%s" % str(auth_code)
                result["result"] = send_email_on_code(msg_text, email)
        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(result))

    def valid_email_tel(self, request):
        result = {}
        try:
            user = request.user
            psd_code = request.GET.get("psd_code")
            valid = request.GET.get("valid")
            if valid == "email":
                try:
                    new_obj = NewUser.objects.get(username=user.username, auth_code=psd_code)
                    self.user_valid = True
                    result["valid"] = True
                    result["username"] = new_obj.username
                except:
                    result["valid"] = False
            else:
                pass

        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(result))

    def modify_password(self, request):
        result = {}
        try:
            password = request.POST.get("password")
            try:
                password = str(password).strip()
                if password == "":
                    raise Exception("密码不合法！")
            except:
                raise Exception("密码不合法！")

            try:
                username = request.user.username
            except:
                raise Exception("用户没有登录！")
            user_valid = self.user_valid
            user = User.objects.get(username=username)
            if user_valid:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                result["modify"] = True
            elif not user.email:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                result["modify"] = True
            else:
                result["modify"] = False
                result["msg"] = "用户身份信息认证失败！"
        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(result))
