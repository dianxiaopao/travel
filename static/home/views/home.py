from django.shortcuts import render

# Create your views here.

try:
    from django.apps import apps as models
except ImportError:  # django < 1.7
    from django.db import models



def Home(request):
    return render(request, 'home.html')

