# -*- coding: utf-8 -*-
import os
from django.conf import settings
from models.sys_material import SysMaterial


class Material(object):
    def __init__(self, model):
        super(Material, self).__init__()
        self.model = model
        self.node_dict = {}
        self.data = [
            {'key': 'user_default_icon_path',
             'value': '/static/media/icon/sysicon/yangwangtiankong.jpg'},
        ]

    def write_data(self):
        data = {}
        for item in self.data:
            key = item.get('key')
            data['value'] = item.get('value')
            new_obj = self.model.objects.get_or_create(key=key, defaults=data)[0]
            new_obj.save()


def make_data():
    from models.sys_material import SysMaterial
    Material(SysMaterial).write_data()
