# -*- coding: utf-8 -*-

from django.conf.urls import url
# import views
#import views.guide as guide_view
import views.guide
# guide =views.guide
urlpatterns = [
    url(r'^$', views.guide.Guide)
]

urls = urlpatterns
