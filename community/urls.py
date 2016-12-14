# -*- coding: utf-8 -*-
from django.conf.urls import url
# import views
#import views.guide as guide_view
import views.community
# guide =views.guide
urlpatterns = [
    url(r'^$', views.community.Community),
    # url(r'^note/create/$', views.mycenter.CreateNote),
]

urls = urlpatterns
