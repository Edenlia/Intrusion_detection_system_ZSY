from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

import json
import datetime

# 导入model中的User
from .models import User, Camera, Case

# 代码编码规则
# 下划线命名法
# 函数名 动作+对象，如更改密码 change——password

import base64
import cv2


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


@csrf_exempt
def test(request):
    img_im = cv2.imread("C://Users//admin//Desktop//cyberpunk2077_cdn_wallpaper.png")
    # img_im = cv2.imread("C://Users//admin//Desktop//202002122048522375731938478.jpg")
    aa = base64.b64encode(cv2.imencode('.jpg', img_im)[1]).decode()
    # aa = base64.b64encode(open("C://Users//admin//Desktop//202002122048522375731938478.jpg", 'rb').read())
    print(aa)  # 17292
    dic = {}
    dic['status'] = 'Success'
    # dic['message']='img'
    dic['img'] = 'data:image/jpg;base64,' + aa
    return HttpResponse(json.dumps(dic))


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
# id username password
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
        username = post_content['username']
        new_password = post_content['password']
        user = User.objects.get(id=user_id)

    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = 'Failed'
        dic['message'] = 'Wrong Id'
        return HttpResponse(json.dumps(dic))
    if username == user.username:
        # 重复密码会报错
        # 从数据库中获取密码检验
        if check_password(new_password, user.password):
            dic['status'] = 'Failed'
            dic['message'] = 'Same Password'
        else:
            user.password = make_password(new_password)
            user.save()
            dic['status'] = 'Success'
    else:
        dic['status'] = 'Failed'
        dic['message'] = "Wrong Username"
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
                        'owner_username': user.username, 'owner_id': user.id
                        }
                # 此处返回owner_id，是为了删除摄像头时，确认owner_id的
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


# 添加摄像头
# name url 外键id
@csrf_exempt
def add_camera(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        name = post_content['name']
        url = post_content['url']
        user_id = post_content['id']
        user = User.objects.get(id=user_id)
        camera = Camera.objects.get(name=name)
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Owner_id"
        return HttpResponse(json.dumps(dic))
    except Camera.DoesNotExist:
        dic['status'] = 'Success'
        new_camera = Camera(name=name, url=url, owner=user)
        new_camera.save()
        return HttpResponse(json.dumps(dic))
    if camera is not None:
        dic['status'] = "Failed"
        dic['message'] = 'Camera Exist'
        return HttpResponse(json.dumps(dic))


# 删除摄像头
# 需要摄像头的一些信息 包括id name owner_id（已移除）
@csrf_exempt
def delete_camera(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        camera_id = post_content['id']
        name = post_content['name']
        camera = Camera.objects.get(id=camera_id)
        if name == camera.name:
            # 名字相同
            camera.delete()
        else:
            dic['status'] = 'Failed'
            dic['message'] = 'Wrong Name'
            return HttpResponse(json.dumps(dic))
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Camera.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))
    dic['status'] = 'Success'
    return HttpResponse(json.dumps(dic))

    # dic = {}
    # if request.method != 'POST':
    #     dic['status'] = "Failed"
    #     dic['message'] = "Wrong Method"
    #     return HttpResponse(json.dumps(dic))
    # try:
    #     post_content = json.loads(request.body)
    #     camera_id = post_content['id']
    #     name = post_content['name']
    #     user_id = post_content['owner_id']
    #
    #     camera = Camera.objects.get(id=camera_id)
    #     user = User.objects.get(id=user_id)
    #
    #     if name == camera.name:
    #         # 名字相同
    #         if user == camera.owner:
    #             # 外键id相同
    #             camera.delete()
    #         else:
    #             dic['status'] = 'Failed'
    #             dic['message'] = 'Wrong Owner'
    #             # 相同的错误信息(待解决)
    #             return HttpResponse(json.dumps(dic))
    #     else:
    #         dic['status'] = 'Failed'
    #         dic['message'] = 'Wrong Name'
    #         return HttpResponse(json.dumps(dic))
    # except(KeyError, json.decoder.JSONDecodeError):
    #     dic['status'] = "Failed"
    #     dic['message'] = "No Input"
    #     return HttpResponse(json.dumps(dic))
    # except Camera.DoesNotExist:
    #     dic['status'] = "Failed"
    #     dic['message'] = "Wrong Id"
    #     return HttpResponse(json.dumps(dic))
    # except User.DoesNotExist:
    #     dic['status'] = 'Failed'
    #     dic['message'] = 'Wrong Owner_id'
    #     return HttpResponse(json.dumps(dic))
    #
    # dic['status'] = 'Success'
    # return HttpResponse(json.dumps(dic))

    # dic = {}
    # if request.method != 'POST':
    #     dic['status'] = "Failed"
    #     dic['message'] = "Wrong Method"
    #     return HttpResponse(json.dumps(dic))
    # try:
    #     post_content = json.loads(request.body)
    #     camera_id = post_content['id']
    #
    #     camera = Camera.objects.get(id=camera_id)
    #     camera.delete()
    # except(KeyError, json.decoder.JSONDecodeError):
    #     dic['status'] = "Failed"
    #     dic['message'] = "No Input"
    #     return HttpResponse(json.dumps(dic))
    # except Camera.DoesNotExist:
    #     dic['status'] = "Failed"
    #     dic['message'] = "Wrong Id"
    #     return HttpResponse(json.dumps(dic))
    #
    # dic['status'] = "Success"
    # return HttpResponse(json.dumps(dic))


# 改变摄像头url
# 传入id name 改变url
@csrf_exempt
def change_url(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        camera_id = post_content['id']
        url = post_content['url']
        name = post_content['name']
        camera = Camera.objects.get(id=camera_id)
        if name == camera.name:
            if url == camera.url:
                dic['status'] = 'Failed'
                dic['message'] = 'Same url'
                return HttpResponse(json.dumps(dic))
            else:
                camera.url = url
                camera.save()
        else:
            dic['status'] = 'Failed'
            dic['message'] = 'Wrong Name'
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Camera.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))

    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))


# 改变摄像头名字
# 传入id name url
@csrf_exempt
def change_name(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        camera_id = post_content['id']
        name = post_content['name']
        url = post_content['url']
        camera = Camera.objects.get(id=camera_id)
        # 验证url
        if url == camera.url:
            if name == camera.name:
                dic['status'] = 'Field'
                dic['message'] = 'Same Name'
            else:
                camera.name = name
                camera.save()
        else:
            dic['status'] = 'Failed'
            dic['message'] = 'Wrong Url'

    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Camera.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))

    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))


# 查询摄像头
# 用户查询自己的摄像头
# id
@csrf_exempt
def query_camera(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        camera_id = post_content['id']
        camera = Camera.objects.get(id=camera_id)

    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Camera.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))
    dic['status'] = "Success"
    dic['id'] = camera.id
    dic['name'] = camera.name
    dic['url'] = camera.url
    return HttpResponse(json.dumps(dic))


# 增加异常信息
# opencv生成
# 入侵情况 tap
@csrf_exempt
def add_case(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        xx = post_content['xx']
        user = User.objects.get(xx=xx)
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


#删除异常信息
@csrf_exempt
def delete_case(request):
    dic={}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        case_id = post_content['id']
        case= Case.objects.get(id=case_id)
        case.delete()
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong id"
        return HttpResponse(json.dumps(dic))

    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))


#改变检阅状态
#传入id 将checked改成1
@csrf_exempt
def change_checked(request):
    dic={}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        case_id = post_content['id']
        case = Case.objects.get(id=case_id)
        case.checked=1
        case.save()
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))

    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))


# 查询摄像头下面的所有的异常信息
# id
@csrf_exempt
def query_all_case(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        camera_id = post_content['id']
        camera = Camera.objects.get(id=camera_id)  # 返回是摄像头名字
        cases = Case.objects.filter(detect_camera=camera).order_by('-date_time')  # 按时间排序
        array = []
        for case in cases:
            dicx = {'id': case.id, 'detect_camera': camera.name, 'checked': case.checked, 'case_type': case.case_type,
                    'case_description': case.case_description, 'level': case.level, 'date_time': case.date_time}
            array.append(dicx)
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Camera.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = 'Failed'
        dic['message'] = 'Wrong Camera'  # 基本不可能
        return HttpResponse(json.dumps(dic))

    dic['status'] = "Success"
    dic['case_list'] = array
    return HttpResponse(json.dumps(dic, cls=DateEncoder))


# 查看单个异常情况信息
# id
# 返回 img
@csrf_exempt
def query_case(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        case_id = post_content['id']
        case = Case.objects.get(id=case_id)
        aa=case.img
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))

    dic['status'] = "Success"
    dic['img']=aa
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
