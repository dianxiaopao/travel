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
             'value': '/static/media/icon/sysicon/yangwangtiankong.jpg',
             'note': u'默认的用户头像'
             },
            {"key": "comm_page_size", "value": "10", "note": u"社区首页展示的帖子的条数"},
            {"key": "sort_page_size", "value": "10", "note": u"分类展示帖子的页数"}
        ]

    def write_data(self):
        data = {}
        for item in self.data:
            key = item.get('key')
            data['value'] = item.get('value')
            data['note'] = item.get('note')
            new_obj = self.model.objects.get_or_create(key=key, defaults=data)[0]
            new_obj.save()


def make_data():
    from models.sys_material import SysMaterial
    Material(SysMaterial).write_data()
