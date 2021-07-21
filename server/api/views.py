from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponse

import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.core.serializers.json import DjangoJSONEncoder

# 导入model中的User
from .models import User


# id permission username password
# 登录验证内容 输入合理 存在账号  密码正确
@csrf_exempt
def login(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        user = User.objects.get(username=username)
        # print( "password: "+password+" user.password: "+user.password)
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Username"
        return HttpResponse(json.dumps(dic))
    if check_password(password, user.password):
        dic['status'] = "Success"
        dic['id'] = user.id
        dic['permission'] = user.permission
        return HttpResponse(json.dumps(dic))
    else:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Password"
        return HttpResponse(json.dumps(dic))

    dic = {'message': "hello"}
    return HttpResponse(json.dumps(dic))


# 注册账号
# method POST
# id permission username password
# 注册逻辑 存在输入 用户不存在进行注册
@csrf_exempt
def register(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        username = post_content['username']
        password = post_content['password']
        user = User.objects.get(username=username)
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Success"
        entry_password = make_password(password)
        new_user = User(username=username, password=entry_password)
        new_user.save()
        return HttpResponse(json.dumps(dic))
    if user is not None:
        dic['status'] = "Failed"
        dic['message'] = "User exist"
        return HttpResponse(json.dumps(dic))
