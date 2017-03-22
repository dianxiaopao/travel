# -*- coding: utf-8 -*-
from django.conf.urls import url
# import views
# import views.guide as guide_view
import views.community_view as communitys

# guide =views.guide
community_view = communitys.Community()
urlpatterns = [
    url(r'^$', community_view.get_community),
    url(r'^view/(?P<category>\w+)/(?P<action>\w+)/$', community_view.get_probem_list),
    url(r'^create/$', community_view.create),
    url(r'^comm/view/(?P<sort>\w+)/(?P<page>\w+)/$', community_view.sort_comm_list),

    url(r'^comm/text/view/(?P<sort>\w+)/(?P<topic>\w+)/$', community_view.view_topic_text),


]

urls = urlpatterns
