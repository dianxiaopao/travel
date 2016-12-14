# -*- coding: utf-8 -*-
from django.conf.urls import url
# import views
#import views.guide as guide_view
import views.home
# guide =views.guide
urlpatterns = [
    url(r'^$', views.home.Home),
    # url(r'^note/create/$', views.mycenter.CreateNote),
]

urls = urlpatterns