# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.db.models import Count
from django.shortcuts import render
from django.db.models.query_utils import Q
from community.models.topic_text import TopicText
from community.models.forum_sort import ForumSort
from base.models.sys_material import SysMaterial
from django.db import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import json, traceback

# Create your views here.

try:
    from django.apps import apps
except ImportError:  # django < 1.7
    from django.db import models as apps


class Community(object):
    def get_community(self, request, *args, **kwargs):
        sort_obj = ForumSort.objects.all()

        def get_edit_data():
            '''
            获取编辑器需要的数据
            :return: default_sort,默认的分类名称，如 综合交流区, edit_box，下拉选择的分类名称
            '''
            edit_box = []
            default_sort = u"没有分类可以选择"
            if sort_obj:
                default_sort = sort_obj[0].id
            for item in sort_obj:
                edit_dict = {}
                edit_dict["name"] = item.name
                edit_dict["id"] = item.id
                edit_box.append(edit_dict)
            return default_sort, edit_box

        default_sort, edit_box = get_edit_data()  # 获取编辑器需要的数据

        def get_sort_data():

            s_n_obj = TopicText.objects.values("forum_sort").annotate(Count('id')).order_by()
            sort_count = {}
            for item in s_n_obj:
                sort_count[str(item["forum_sort"])] = item["id__count"]

            sort_list = []
            for item in sort_obj:
                if item.a_public:
                    sort_dict = {}
                    new_comm = sort_count[str(item.id)] if sort_count.has_key(str(item.id)) else 0
                    sort_dict = {
                        "name": item.name,
                        "describe": item.describe,
                        "url": item.url,
                        "icon": item.icon,
                        "new_comm": new_comm,
                    }
                    sort_list.append(sort_dict)

            return sort_list

        sort_list = get_sort_data()

        filter_str = {'forum_sort_id': 1}

        comm_list = self._get_commit_list(request, 1, 10, filter_str, None)
        context = {
            'edit_box': edit_box,
            'default_sort': default_sort,
            'sort_list': sort_list,
            'comm_list': comm_list,
        }
        return render(request, 'community.html', context)

    def _get_commit_list(self, request, page, page_size, filter_str, order_str):
        if not order_str:
            order_str = "write_date"
        page_start = page - 1
        page_end = page_size * page + page - 2
        comm_obj = TopicText.objects.filter(Q(**filter_str) & Q(**{"a_public": True})).order_by("priority").order_by(
            order_str)[page_start: page_end]
        comm_list = []
        icon_obj = SysMaterial.objects.get(key='user_default_icon_path')
        icon_path = icon_obj.value
        for item in comm_obj:
            comm_dict = {}
            comm_dict["user_icon"] = icon_path
            if item.write_user:
                if isinstance(item.write_user, models.Model):
                    pass  # 如果用户头像存在则改变头像
            comm_dict["name"] = item.name
            comm_dict["text"] = item.text
            comm_dict['date'] = item.write_date
            comm_list.append(comm_dict)
        return comm_list

    def get_probem_list(self, request, *args, **kwargs):
        category = kwargs.get("category")
        action = kwargs.get("action")

    # @method_decorator(login_required)
    def create(self, request):
        method = request.method.lower()
        if method == 'post':
            result = {}
            try:
                if request.user.is_authenticated():
                    comm_sort = request.POST.get("comm_sort")
                    comm_text = request.POST.get("comm_text")
                    comm_title = request.POST.get("comm_title").strip()
                    if not comm_sort:
                        raise Exception("请选择分类")
                    if not comm_text:
                        raise Exception("请输入内容")
                    if not comm_title:
                        raise Exception("输入标题")
                    new_obj = TopicText(
                        name=comm_title,
                        text=comm_text,
                        forum_sort_id=comm_sort,
                        create_user=request.user,
                        write_user=request.user
                    )
                    TopicText.objects.bulk_create([new_obj])
                    result["successful"] = True
                    result["title"] = comm_title
                else:
                    result['next']='/login/'
            except Exception, e:
                _trackback = traceback.format_exc()
                err_msg = e.message
                if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                    err_msg = e.faultCode
                result['error_msg'] = err_msg
                result['trackback'] = _trackback
            finally:
                return HttpResponse(json.dumps(result))
