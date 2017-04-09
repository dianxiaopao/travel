# -*- coding: utf-8 -*-
from django.conf.urls import url

import views.home

home_view = views.home.Home()

urlpatterns = [
    url(r'^(?P<username>\w+)/$', home_view.home),
]

urls = urlpatterns
