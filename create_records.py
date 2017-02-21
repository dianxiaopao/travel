# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
user = User.objects.create_user(username='admin',password='admin',email='admin@gaomumu.com')
user.save