from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

try:
    from django.apps import apps as models
except ImportError:  # django < 1.7
    from django.db import models


class Home(object):
    def home(self, request, *args, **kwargs):
        username = kwargs.get("username")
        try:
            user_obj = User.objects.get(username=username)
        except:
            return render(request, 'login.html')
        return render(request, 'home.html')
