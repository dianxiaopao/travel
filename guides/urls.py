# -*- coding: utf-8 -*-

from django.conf.urls import url
# import views
#import views.guide as guide_view
import views.guide
# guide =views.guide
urlpatterns = [
    url(r'^(?P<page>\w+)/$', views.guide.Guide),
    url(r'^view/(?P<id>\w+)/$', views.guide.view_essay)
]

urls = urlpatterns
