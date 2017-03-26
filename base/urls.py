# -*- coding: utf-8 -*-

from django.conf.urls import url
# import views
# import views.guide as guide_view
import views.upload_views as upload_views

upload_view = upload_views.Upload()
# guide =views.guide
urlpatterns = [
    url(r'^upload_img/$', upload_view.edit_upload_image),
]

urls = urlpatterns
