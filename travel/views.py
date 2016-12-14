# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,Http404
try:
	from django.apps import apps as models
except ImportError:  # django < 1.7
	from django.db import models

import json


def index(request):
    return render(request,'index.html')

