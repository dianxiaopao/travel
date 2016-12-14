# -*- coding: utf-8 -*-
from django.shortcuts import render
from mycenter.models.img_material import ImgMaterial
from django.http import HttpResponse, Http404

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


# class myCenterView(object):

def title_img(request):
    models = ImgMaterial
    method = request.method.lower()
    if method == 'post':
        try:
            result = {}
            file = request.FILES.get('files[]')
            uuid_name = shortuuid.uuid()
            image_name = uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid_name))
            file_dir = os.path.join(travel.settings.MEDIA_ROOT, 'OldImgFile')
            if os.path.exists(file_dir) == False:
                os.makedirs(file_dir)
            old_file_name = str(image_name) + str('.') + str(file.name.split('.')[-1])

            file_path = os.path.join(file_dir, old_file_name)
            fobj = open(file_path, 'wb')
            for chrunk in file.chunks():
                filecontent = base64.b64encode(chrunk)
                fobj.write(filecontent)
            fobj.close()
            new_obj = models.objects.get_or_create(alias=old_file_name)[0]
            new_obj.name = file.name
            new_obj.alias = old_file_name
            new_obj.old_path = file_dir
            new_obj.save()
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


@csrf_exempt
def show_title_img(request):
    models = ImgMaterial
    method = request.method.lower()
    if method == 'post':
        result = {}
        try:
            image_alias = request.POST.get('alias')
            image_old_path = os.path.join(request.POST.get('old_path'), image_alias)
            relative_path = os.path.join('static', 'media', 'images', image_alias)
            image_new_path = os.path.join(travel.settings.BASE_DIR, relative_path)
            with open(image_old_path) as f:
                temporary_file = open(image_new_path, 'wb')
                temporary_file.write(base64.b64decode(f.read()))
                temporary_file.close()

            new_obj = models.objects.filter(alias=image_alias)[0]
            new_obj.new_path = os.path.join(travel.settings.BASE_DIR, 'static', 'media', 'images')
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
