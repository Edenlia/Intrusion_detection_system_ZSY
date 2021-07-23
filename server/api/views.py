from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponse

import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

import datetime
from django.core.serializers.json import DjangoJSONEncoder

# 导入model中的User
from .models import User, Camera


# 代码编码规则
# 下划线命名法
# 函数名 动作+对象，如更改密码 change——password


# def test(request):
#     return HttpResponse("result")


# #函数模板
# @csrf_exempt
# def xxx(request):
#     dic={}
#     if request.method != 'POST':
#         dic['status'] = "Failed"
#         dic['message'] = "Wrong Method"
#         return HttpResponse(json.dumps(dic))
#     try:
#         post_content = json.loads(request.body)
#         xx = post_content['xx']
#         user = User.objects.get(xx=xx)
#     except(KeyError, json.decoder.JSONDecodeError):
#         dic['status'] = "Failed"
#         dic['message'] = "No Input"
#         return HttpResponse(json.dumps(dic))
#     except User.DoesNotExist:
#         dic['status'] = "Failed"
#         dic['message'] = "Wrong Username"
#         return HttpResponse(json.dumps(dic))
#
#     dic['status'] = "Success"
#     return HttpResponse(json.dumps(dic))


# id permission username password
# 登录验证内容 输入合理 存在账号  密码正确
# 返回id
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

    # dic = {'message': "hello"}
    # return HttpResponse(json.dumps(dic))


# 注册账号
# method POST
# username password
# 注册逻辑 存在输入 用户不存在进行注册
# 要求：
# 重复用户检测
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


# 注销账号
# 提供id注销
#   先检测摄像头存在，删除摄像头
#   再删除账号
@csrf_exempt
def delete_account(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = 'Wrong Method'
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        user_id = post_content['id']
        user = User.objects.get(id=user_id)
        camera = Camera.objects.filter(owner=user)
        if len(camera) is not 0:
            for c in camera:
                c.delete()
        user.delete()
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = 'Failed'
        dic['message'] = 'Wrong id'
        return HttpResponse(json.dumps(dic))

    dic['status'] = 'Success'
    return HttpResponse(json.dumps(dic))


# 更改用户名
#   id正确
#   更改后的用户名不存在
@csrf_exempt
def change_username(request):
    dic = {}
    if request.method == 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        user_id = post_content['id']
        user = User.objects.get(id=user_id)
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Username"
        return HttpResponse(json.dumps(dic))

    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))


# 更改密码
# 根据用户主键id更改
@csrf_exempt
def change_password(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = 'Wrong Method'
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        user_id = post_content['id']
        new_password = post_content['password']
        user = User.objects.get(id=user_id)
        user.password = make_password(new_password)
        user.save()
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = 'Failed'
        dic['message'] = 'Wrong id'
        return HttpResponse(json.dumps(dic))

    dic['status'] = 'Success'
    return HttpResponse(json.dumps(dic))

    # dic = {'message': "hello"}
    # return HttpResponse(json.dumps(dic))s


# 查询所有的用户
@csrf_exempt
def query_all(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        permission = post_content['permission']
        # user = User.objects.filter(permission=permission)
        users = User.objects.filter(permission=permission)
        array = []
        for user in users:
            dics = {'id': user.id, "username": user.username}
            array.append(dics)
        # print(array)
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Username"
        return HttpResponse(json.dumps(dic))

    dic['status'] = "Success"
    dic['user_list'] = array
    # dic['id'] = list(user.values('id'))
    # dic['username'] = list(user.values('username'))
    return HttpResponse(json.dumps(dic))


# 查询独立用户
# 查询一个用户， 并返回用户所用的所有摄像头
# 根据id 查询
@csrf_exempt
def query_user(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        user_id = post_content['id']
        user = User.objects.get(id=user_id)
        cameras = Camera.objects.filter(owner=user)  # filter不会触发摄像头
        array = []
        if len(cameras) is not 0:
            for camera in cameras:
                disc = {'id': camera.id, 'name': camera.name, 'url': camera.url, 'description': camera.description,
                        'owner_username': user.username
                        }
                array.append(disc)
            dic['status'] = "Success"
            dic['camera_list'] = array
        else:
            dic['status'] = "Success"
            dic['camera_list'] = 'No Exist Camera'
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Username"
        return HttpResponse(json.dumps(dic))

    return HttpResponse(json.dumps(dic))


# 添加管理员账号
# post  id
@csrf_exempt
def add_admin(request):
    dic = {}
    if request.method == 'GET':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        user_id = post_content['id']
        user = User.objects.get(id=user_id)
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = 'Not Exist user'
        return HttpResponse(json.dumps(dic))
    # 查看用户权限
    if user.permission == '1':
        dic['status'] = 'Failed'
        dic['message'] = 'No user'
        return HttpResponse(json.dumps(dic))
    else:
        user.permission = 1
        user.save()
        dic['status'] = 'Successes'
        return HttpResponse(json.dumps(dic))
