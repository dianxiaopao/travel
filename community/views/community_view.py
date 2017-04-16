# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.shortcuts import render
from django.db.models.query_utils import Q
from community.models.topic_text import TopicText
from community.models.forum_sort import ForumSort
from base.models.sys_material import SysMaterial
from community.models.comment import Comment

from django.db import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from base.views.base_views import UserView
import base.views.base_views as base_view

get_user_data = base_view.UserView().get_user_data

import json, traceback, pytz

# Create your views here.

try:
    from django.apps import apps
except ImportError:  # django < 1.7
    from django.db import models as apps


class Community(object):
    def get_questions_list(self, request):
        sort_id = request.GET.get("sort")
        page = request.GET.get("page")
        page_obj = SysMaterial.objects.filter(key="comm_page_size")
        page_size = int(page_obj[0].value) if page_obj else 10
        order_field = "write_date"
        filter_str = {'u_public': True, "a_public": True}
        try:
            page = int(page)
        except:
            pass
        if sort_id != "all":
            try:
                sort_id = int(sort_id)
                if sort_id in self.sort_ids:
                    filter_str["forum_sort_id"] = sort_id
            except:
                pass
        text_obj = TopicText.objects.filter(Q(**filter_str)).order_by("priority").order_by(order_field)[
                   page * page_size:(page + 1) * page_size]
        user_ids = []
        text_ids = []
        for item in text_obj:
            text_ids.append(item.id)
            user_ids.append(item.write_user_id)
        user_data = get_user_data(user_ids)
        # 评论数量还没有
        questions = []
        for item in text_obj:
            text_txt = item.text_txt[:75] if item.text_txt else ""
            new_date = item.write_date.astimezone(pytz.timezone('Asia/Shanghai'))
            write_date = str(new_date)[:19]
            write_user = user_data[item.write_user_id]
            show_name = write_user["show_name"] if write_user["show_name"] else write_user["username"]
            q_dict = {
                "id": item.id,
                "title": item.name,
                "text_htm": item.text_htm,
                "text_txt": text_txt,
                "pviews": item.pviews,
                "collection": item.collection,
                "write_date": write_date,
                "show_name": show_name,
                "signatrue": write_user["signatrue"],
            }
            questions.append(q_dict)
        return questions

    def get_community(self, request):
        sort = request.GET.get("sort")
        self.page = 0
        sort_obj = ForumSort.objects.all()
        self.sort_obj = sort_obj
        edit_box = []
        default_sort = u"没有分类可以选择"
        if sort_obj:
            default_sort = sort_obj[0].id
        sort_ids = []
        for item in sort_obj:
            sort_ids.append(item.id)
            edit_dict = {
                "name": item.name,
                "id": item.id
            }
            edit_box.append(edit_dict)
        self.sort_ids = sort_ids

        user_data = get_user_data(request.user)
        # questions = self.get_questions_list(request)
        context = {
            'edit_box': edit_box,
            'default_sort': default_sort,
            # 'questions': questions
        }
        return render(request, 'community.html', context)

    def get_question_list(self, request):
        questions = self.get_questions_list(request)
        context = {
            'questions': questions
        }
        return render(request, 'question_list.html', context)

    def _get_commit_list(self, page, page_size, filter_str, order_str):
        if not order_str:
            order_str = "write_date"
        page_start = page - 1
        page_end = page_size * page + page - 2
        if not filter_str:
            comm_obj = TopicText.objects.filter(Q(**{"a_public": True})).order_by("priority").order_by(order_str)[
                       page_start: page_end]
        else:
            comm_obj = TopicText.objects.filter(Q(**filter_str) & Q(**{"a_public": True})).order_by(
                "priority").order_by(order_str)[page_start: page_end]
        comm_list = []
        icon_obj = SysMaterial.objects.get(key='user_default_icon_path')
        icon_path = icon_obj.value
        for item in comm_obj:
            comm_dict = {}
            comm_dict["user_icon"] = icon_path
            if item.write_user:
                user = item.write_user
                if isinstance(item.write_user, models.Model):
                    pass  # 如果用户头像存在则改变头像
            comm_dict["name"] = item.name
            comm_dict["text"] = item.text
            comm_dict["id"] = item.id
            comm_dict['date'] = item.write_date
            comm_dict['collection'] = item.collection
            comm_dict['pviews'] = item.pviews
            comm_dict['sort_id'] = item.forum_sort_id
            comm_dict['user'] = user
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
                    comm_sort = request.POST.get("question_sort")
                    comm_text = request.POST.get("question_main_text")
                    comm_html = request.POST.get("question_main_html")
                    comm_title = request.POST.get("question_title").strip()
                    if not comm_sort:
                        raise Exception("请选择分类")
                    if not comm_text:
                        raise Exception("请输入内容")
                    if not comm_title:
                        raise Exception("输入标题")
                    new_obj = TopicText(
                        name=comm_title,
                        text_txt=comm_text,
                        text_htm=comm_html,
                        forum_sort_id=comm_sort,
                        create_user=request.user,
                        write_user=request.user
                    )
                    TopicText.objects.bulk_create([new_obj])
                    result["successful"] = True
                    result["title"] = comm_title.encode("utf-8")
                else:
                    result['next'] = '/login/'
            except Exception, e:
                _trackback = traceback.format_exc()
                err_msg = e.message
                if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                    err_msg = e.faultCode
                result['error_msg'] = err_msg
                result['trackback'] = _trackback
            finally:
                return HttpResponse(json.dumps(result))

    def sort_comm_list(self, request, *args, **kwargs):
        result = {}
        sort = kwargs.get("sort")
        page = kwargs.get("page")
        try:
            sort = int(sort)
            page = int(page)
        except:
            return HttpResponseRedirect('404.html')
        size_obj = SysMaterial.objects.filter(key="sort_page_size")
        page_size = int(size_obj[0].value) if size_obj else 10
        filter_str = {"forum_sort_id": sort}
        comm_list = self._get_commit_list(page, page_size, filter_str, None)

        context = {
            'comm_list': comm_list,
        }
        return render(request, 'topic_text_list.html', context)

    def view_topic_text(self, request, *args, **kwargs):
        topic_id = kwargs.get("topic")
        text = {}
        text_obj = TopicText.objects.filter(id=topic_id)
        icon_obj = SysMaterial.objects.get(key='user_images_default')
        icon_path = icon_obj.value
        if not text_obj:
            return HttpResponseRedirect('404.html')
        text_obj = text_obj[0]
        user = text_obj.write_user
        if hasattr(user, "newuser"):
            pass  # 如果用户头像存在则改变头像
        text["title"] = text_obj.name
        text["text"] = text_obj.text_htm
        # text["pviews"] = text_obj[0].pviews             #评论数
        text["collection"] = text_obj.collection  # 收藏
        text["user_icon"] = icon_path
        text["user_name"] = request.user.username

        comm_obj = Comment.objects.filter(parent_id=text_obj.id, parent_type="TopicText", is_active=True,
                                          parent_comment=None)
        sum_comment = len(comm_obj)
        comm_list = []
        l1_comment_ids = []
        for item in comm_obj:
            l1_comment_ids.append(item.id)
            comm_dict = {"content": item.content}
            comm_dict["id"] = item.id
            if hasattr(item.write_user, "newuser"):
                pass  # 如果用户头像存在则改变头像
            comm_dict["user_name"] = item.write_user.username
            comm_dict["user_icon"] = icon_path
            comm_list.append(comm_dict)
        count_l2_obj = Comment.objects.filter(parent_comment__in=l1_comment_ids).values("parent_comment").annotate(
            Count('parent_comment'))
        # 获取子评论数
        count_comment = {}
        for item in count_l2_obj:
            count_comment[item["parent_comment"]] = item["parent_comment__count"]
        # 把子评论数写入到模板参数中
        for item in comm_list:
            if count_comment.has_key(item["id"]):
                item["sub_number"] = count_comment[item["id"]]
            else:
                item["sub_number"] = 0
        context = {
            "text": text,
            "parent_type": "TopicText",
            "parent_id": text_obj.id,
            "comm_list": comm_list,
            "sum_comment": sum_comment,
        }
        return render(request, "topic_text_view.html", context)
