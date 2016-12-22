# -*- coding: utf-8 -*-
from django.shortcuts import render
from mycenter.models.img_material import ImgMaterial

from guides.models.guide_title import GuideTitle
from guides.models.guide_content import Guidebody
from django.http import HttpResponse, Http404
from django.conf import settings

import json, uuid, shortuuid, os, base64, travel.settings, traceback
from django.views.decorators.csrf import csrf_exempt


def Center(request):
    return render(request, 'center.html')


@csrf_exempt
def CreateNote(request):
    article_uuid = shortuuid.uuid
    context = {
        'uuid': article_uuid,
        'action': 'create',
    }
    return render(request, 'create_note.html', context)


def title_img(request):
    models = ImgMaterial
    method = request.method.lower()

    if method == 'post':
        result = {}
        try:

            f = request.FILES.get('files[]')

            uuid_name = shortuuid.uuid()
            image_name = uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid_name))
            file_dir = os.path.join(settings.MEDIA_ROOT, 'OldImgFile')
            if os.path.exists(file_dir) == False:  # 如果文件夹不存在就创建它
                os.makedirs(file_dir)

            img_alias = str(image_name) + str('.') + str(f.name.split('.')[-1])

            file_path = os.path.join(file_dir, img_alias)
            fobj = open(file_path, 'wb')
            for chrunk in f.chunks():
                filecontent = base64.b64encode(chrunk)
                fobj.write(filecontent)
            fobj.close()  # 文件保存完毕

            # 把文件信息写到数据库
            img_d_obj = {
                'name': f.name, 'file_size': f.size, 'old_path': file_dir, 'alias': img_alias
            }
            new_obj = models.objects.get_or_create(alias=img_alias, defaults=img_d_obj)[0]
            new_obj.save()  # 把上传的图片信息保存到数据库中

            title_uuid = request.POST.get('uuid')
            title = request.POST.get('guide_title')
            title_obj = GuideTitle.objects.filter(uuid=title_uuid)
            if len(title_obj) == 0:
                title_obj = GuideTitle(uuid=title_uuid, source='user create', title_img_id=new_obj.id)
                if title != '':
                    title_obj.title = str(title)
                title_obj.save()
            else:
                title_obj[0].title_img_id = new_obj.id
                if title != '':
                    title_obj.title = title
                title_obj[0].save()
            result['alias'] = new_obj.alias
            result['old_path'] = file_dir
        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(result))

    if method == 'get':
        return HttpResponse(json.dumps('对不起没有get请求的的后台'))


# @csrf_exempt
def show_title_img(request):
    models = ImgMaterial
    method = request.method.lower()
    if method == 'post':
        result = {}
        try:
            image_alias = request.POST.get('alias')
            image_old_path = os.path.join(request.POST.get('old_path'), image_alias)
            relative_path = os.path.join('static', 'media', 'images', image_alias)
            image_new_path = os.path.join(settings.BASE_DIR, relative_path)
            with open(image_old_path) as f:
                temporary_file = open(image_new_path, 'wb')
                temporary_file.write(base64.b64decode(f.read()))
                temporary_file.close()

            new_obj = models.objects.filter(alias=image_alias)[0]
            new_obj.new_path = os.path.join(settings.BASE_DIR, 'static', 'media', 'images')
            new_obj.save()
            result['path'] = relative_path
        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(result))

    elif method == 'get':
        pass


def create_title(request):
    method = request.method.lower()
    if method == 'post':
        result = {}
        try:
            title_uuid = request.POST.get('uuid')
            title = request.POST.get('title')
            title_obj = GuideTitle.objects.filter(uuid=title_uuid)
            if title != '':
                if len(title_obj) == 0:
                    title_obj = GuideTitle(uuid=title_uuid, source='user create', title=title)
                    title_obj.save()
                else:
                    title_obj[0].title = title
                    title_obj[0].save()
                result['success'] = title
            else:
                result['success'] = u'标题未做改变'

        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(result))

    elif method == 'get':
        pass


def upload_file(f):
    res_and_obj = {}
    result = {}
    uuid_name = shortuuid.uuid()
    image_name = uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid_name))
    file_dir = os.path.join(settings.MEDIA_ROOT, 'OldImgFile')
    if os.path.exists(file_dir) == False:  # 如果文件夹不存在就创建它
        os.makedirs(file_dir)

    img_alias = str(image_name) + str('.') + str(f.name.split('.')[-1])

    file_path = os.path.join(file_dir, img_alias)
    fobj = open(file_path, 'wb')
    for chrunk in f.chunks():
        filecontent = base64.b64encode(chrunk)
        fobj.write(filecontent)
    fobj.close()  # 文件保存完毕

    # 把文件信息写到数据库
    img_d_obj = {
        'name': f.name, 'file_size': f.size, 'old_path': file_dir, 'alias': img_alias
    }
    new_obj = ImgMaterial.objects.get_or_create(alias=img_alias, defaults=img_d_obj)[0]
    # 解码到static文件下
    relative_path = os.path.join('static', 'media', 'images', img_alias)
    image_new_path = os.path.join(settings.BASE_DIR, relative_path)
    with open(file_path) as f:
        temporary_file = open(image_new_path, 'wb')
        temporary_file.write(base64.b64decode(f.read()))
        temporary_file.close()
    new_obj.new_path = os.path.join(settings.BASE_DIR, 'static', 'media', 'images')
    new_obj.save()
    result['path'] = relative_path
    res_and_obj['result'] = result
    res_and_obj['file_obj'] = new_obj
    return res_and_obj


@csrf_exempt
def upload_img(request):
    result = {}
    method = request.method.lower()
    if method == 'post':
        try:
            f = request.FILES.get('files')
            res_and_obj = upload_file(f)
            img_obj = res_and_obj['file_obj']

            uuid = request.GET.get("uuid")
            title_obj = GuideTitle.objects.get_or_create(uuid=uuid)[0]
            title_obj.source = 'user create'
            title_obj.save()
            body_uuid = shortuuid.uuid()
            body_text = Guidebody(uuid=body_uuid, title_id=title_obj.id, image_path=img_obj.new_path,
                                  image_name=img_obj.name)
            body_text.image_location = 'all'
            body_text.save()
            result["img_uuid"] = body_text.uuid






        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(res_and_obj['result']))

    if method == 'get':
        return HttpResponse(json.dumps('对不起没有get请求的的后台'))


def edit_text(request):
    result = {}
    method = request.method.lower()
    if method == 'post':
        try:
            uuid = request.POST.get("title_uuid")
            text_val = request.POST.get("text")
            body_uuid = request.POST.get("body_uuid")

            title_obj = GuideTitle.objects.get_or_create(uuid=uuid)[0]
            title_obj.source = 'user create'
            title_obj.save()
            if body_uuid:
                body_obj = Guidebody.objects.filter(uuid=body_uuid,title_id=title_obj.id)
                if body_obj:
                    body_obj[0].s_body = text_val
                    body_obj[0].title_obj.id
                    body_obj[0].save()
                    result["body_uuid"] = body_obj.uuid
                    result["text"] = body_obj.s_body
                else:
                    body_uuid = shortuuid.uuid()
                    body_obj = Guidebody(uuid=body_uuid, s_body=text_val, title_id=title_obj.id)
                    body_obj.save()
                    result["body_uuid"] = body_obj.uuid
                    result["text"] = body_obj.s_body
            else:
                body_uuid = shortuuid.uuid()
                body_obj = Guidebody(uuid=body_uuid, s_body=text_val, title_id=title_obj.id)
                body_obj.save()
                result["body_uuid"] = body_obj.uuid
                result["text"] = body_obj.s_body
        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(result))
