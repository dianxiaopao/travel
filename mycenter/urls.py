# -*- coding: utf-8 -*-
from django.conf.urls import url
# import views
# import views.guide as guide_view
import views.mycenter_vilews
# import views.mycenter_vilews as myCenterViews
# mycenterviews=myCenterViews.myCenterView

# guide =views.guide
urlpatterns = [
    url(r'^$', views.mycenter_vilews.Center),
    url(r'^note/create/$', views.mycenter_vilews.CreateNote),
    url(r'^note/create/upload_title_img/$', views.mycenter_vilews.title_img),
    url(r'^note/create/show_title_img/$', views.mycenter_vilews.show_title_img),
]

urls = urlpatterns
