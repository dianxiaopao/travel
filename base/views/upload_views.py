# -*- coding: utf-8 -*-
from base.models.sys_material import SysMaterial
from mycenter.models.img_material import ImgMaterial
from django.http import HttpResponse, Http404, StreamingHttpResponse
from django.conf import settings
import traceback, json, os, base64, uuid, responses
from utils import switch_path_relative

try:
    from django.apps import apps
except ImportError:  # django < 1.7
    from django.db import models as apps


class Upload(object):
    def edit_upload_image(self, request):
        result = None
        try:
            file_obj = request.FILES.get("wangEditorH5File")
            if not file_obj:
                raise Exception("没有获取到文件对象！")
            path_obj = SysMaterial.objects.filter(key="image_path")
            if not path_obj:
                raise Exception("没有配置文件上传路径！")

            if not request.user.is_authenticated():
                raise Exception("登录用户才可以上传文件！")
            user = request.user
            file_name = str(uuid.uuid1()) + "_" + user.username + '.' + str(file_obj.name.split('.')[-1])
            folder = os.path.join(settings.BASE_DIR, path_obj[0].value, "media", "editor")
            if not os.path.exists(folder):
                os.makedirs(folder)
            path = os.path.join(folder, file_name)
            # 保存文件
            b64_folder = os.path.join(settings.BASE_DIR, path_obj[0].value, "media", "editor", "b64")
            if not os.path.exists(folder):
                os.makedirs(b64_folder)
            b64_path = os.path.join(b64_folder, file_name)
            fobj = open(b64_path, 'wb')
            for ck in file_obj.chunks():
                f = base64.b64encode(ck)
                fobj.write(f)
            fobj.close()  # 文件保存完毕

            new_obj = open(path, 'wb')
            with open(b64_path) as f:
                new_obj.write(base64.b64decode(f.read()))
            new_obj.close()
            f.close()
            img_obj = ImgMaterial(
                name=file_obj.name,
                alias=file_name,
                old_path=b64_path,
                new_path=path,
                file_size=file_obj.size,
                source="user_upload",
                create_user=user,
                write_user=user
            )
            ImgMaterial.objects.bulk_create([img_obj])
            static_path = switch_path_relative(path, path_obj[0].value)
            result = static_path.encode("utf8")
        except Exception, e:
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result = "error|" + err_msg
        finally:
            return HttpResponse(result)
