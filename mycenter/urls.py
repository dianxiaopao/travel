# -*- coding: utf-8 -*-
from django.conf.urls import url

import views.mycenter_vilews

urlpatterns = [
    url(r'^$', views.mycenter_vilews.Center),
    url(r'^note/create/$', views.mycenter_vilews.CreateNote),
    url(r'^note/create/upload_title_img/$', views.mycenter_vilews.title_img),
    url(r'^note/create/show_title_img/$', views.mycenter_vilews.show_title_img),
    url(r'^note/create/create_title/$', views.mycenter_vilews.create_title),
    url(r'^note/create/upload_img/$', views.mycenter_vilews.upload_img),
    url(r'^note/create/edit_text/$', views.mycenter_vilews.edit_text),
    url(r'^note/create/edit_text_get/$', views.mycenter_vilews.edit_text_get),
]

urls = urlpatterns
