# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

try:
    from django.apps import apps as models
except ImportError:  # django < 1.7
    from django.db import models


class Community(object):
    def get_community(self, request, *args, **kwargs):
        return render(request, 'community.html')

    def get_probem_list(self, request, *args, **kwargs):
        category = kwargs.get("category")
        action = kwargs.get("action")
