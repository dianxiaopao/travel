# -*- coding: utf-8 -*-
from django.conf.urls import url

import views.home

home_view = views.home.Home()

urlpatterns = [
    url(r'^people/(?P<username>\w+)/$', home_view.home),
    url(r'^setting/$', home_view.settings),
    url(r'^setting/get_email_code/$', home_view.get_email_code),
    url(r'^setting/save_new_email/$', home_view.save_new_email),
    url(r'^setting/send_valid_code/$', home_view.send_valid_code),
    url(r'^setting/valid_email_tel/$', home_view.valid_email_tel),
    url(r'^setting/modify_password/$', home_view.modify_password),
]

urls = urlpatterns
