from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import datetime
from django.utils import timezone
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
    dic = {'status': 'Success', 'img': 'data:image/jpg;base64,' + aa}
    # dic['message']='img'

    'male 18-24'
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
                disc = {'id': camera.id, 'name': camera.name, 'type': camera.type, 'url': camera.url,
                        'description': camera.description,
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
# @csrf_exempt
# def add_case(request):
#     dic = {}
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

# 删除异常信息
@csrf_exempt
def delete_case(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        case_id = post_content['id']
        case = Case.objects.get(id=case_id)
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


# 改变检阅状态
# 传入id 将checked改成1
@csrf_exempt
def change_checked(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        case_id = post_content['id']
        case = Case.objects.get(id=case_id)
        case.checked = 1
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
        user_id = post_content['id']
        user = User.objects.get(id=user_id)
        cameras = Camera.objects.filter(owner=user)  # 返回是摄像头名字
        array = []
        if len(cameras) is not 0:
            for camera in cameras:
                cases = Case.objects.filter(detect_camera=camera).order_by('-date_time')  # 按时间排序
                if len(cases) is not 0:
                    for case in cases:
                        dicx = {'id': case.id, 'detect_camera': camera.name, 'checked': case.checked,
                                'case_type': case.case_type,
                                'case_description': case.case_description, 'level': case.level,
                                'date_time': case.date_time}
                        array.append(dicx)
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))
    except Camera.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong user_id"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = 'Failed'
        dic['message'] = 'Wrong Camera'  # 基本不可能
        return HttpResponse(json.dumps(dic))

    dic['status'] = "Success"
    dic['case_list'] = sorted(array, key=lambda i: (i['date_time']))
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
        dic['status'] = "Success"
        dic['id'] = case_id
        dic['checked'] = case.checked
        dic['case_type'] = case.case_type
        dic['level'] = case.level
        dic['date_time'] = case.date_time
        dic['img'] = case.img
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))

    return HttpResponse(json.dumps(dic, cls=DateEncoder))


# 统计一个月早中晚入侵人数
# 查询数据库中一个月的内容
@csrf_exempt
def count_human_all(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=30)
        # --gt 大于 --gte大于等于 datetime 递增
        cases = Case.objects.filter(date_time__gte=start, case_type=2)
        morning = noon = evening = 0
        # 4-11 11-18 18-04
        for case in cases:
            # dicx=case.date_time.strftime('%S-%M-%H-%Y-%m-%d')
            dicx = case.date_time.strftime('%H')
            hour = int(dicx)
            if 0 <= hour < 4:
                evening = evening + 1
            elif 4 <= hour < 11:
                morning = morning + 1
            elif 11 <= hour < 18:
                noon = noon + 1
            else:
                evening = evening + 1
        dic['status'] = "Success"
        dic['morning'] = morning
        dic['noon'] = noon
        dic['evening'] = evening
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Empty Case"
        return HttpResponse(json.dumps(dic))

    return HttpResponse(json.dumps(dic))


# 一个月内早中晚入侵车辆统计
@csrf_exempt
def count_car_all(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=30)
        cases = Case.objects.filter(date_time__gte=start, case_type=1)
        morning = noon = evening = 0
        for case in cases:
            dicx = case.date_time.strftime('%H')
            hour = int(dicx)
            if 0 <= hour < 4:
                evening = evening + 1
            elif 4 <= hour < 11:
                morning = morning + 1
            elif 11 <= hour < 18:
                noon = noon + 1
            else:
                evening = evening + 1
        dic['status'] = "Success"
        dic['morning'] = morning
        dic['noon'] = noon
        dic['evening'] = evening
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Empty Case"
        return HttpResponse(json.dumps(dic))

    return HttpResponse(json.dumps(dic))


# 统计一周内每天新注册用户
@csrf_exempt
def count_user_register(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=7)
        users = User.objects.filter(date_time__gte=start)
        # monday = tuesday = wednesday = thursday = friday = saturday = sunday = 0
        dic['status'] = "Success"
        dic['monday'] = dic['tuesday'] = dic['wednesday'] = dic['thursday'] = dic['friday'] = dic['saturday'] = dic[
            'sunday'] = 0
        for user in users:
            day = user.date_time.weekday()  # 0-6 星期一到星期日
            if day == 0:
                # monday = monday + 1
                dic['monday'] = dic['monday'] + 1
            elif day == 1:
                # tuesday = tuesday + 1
                dic['tuesday'] = dic['tuesday'] + 1
            elif day == 2:
                # wednesday = wednesday + 1
                dic[' wednesday'] = dic[' wednesday'] + 1
            elif day == 3:
                # thursday = thursday + 1
                dic['thursday'] = dic['thursday'] + 1
            elif day == 4:
                # friday = friday + 1
                dic['friday'] = dic['friday'] + 1
            elif day == 5:
                # saturday = saturday + 1
                dic['saturday'] = dic['saturday'] + 1
            elif day == 6:
                # sunday = sunday + 1
                dic['sunday'] = dic['sunday'] + 1

    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Empty User"
        return HttpResponse(json.dumps(dic))

    return HttpResponse(json.dumps(dic))


#   一月内入侵人员年龄统计(用户)
#   传入用户id，查看所属摄像头，再搜索摄像头有的异常，再统计异常情况
@csrf_exempt
def count_human_age(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        user_id = post_content['id']
        user = User.objects.get(id=user_id)
        cameras = Camera.objects.filter(owner=user)
        dic['status'] = 'Success'
        dic['0-18'] = dic['18-45'] = dic['45-65'] = dic['65-100'] = 0
        for camera in cameras:
            now = datetime.datetime.now()
            start = now - datetime.timedelta(days=30)
            cases = Case.objects.filter(date_time__gte=start, case_type=2, detect_camera_id=camera)
            for case in cases:
                dicx = {}
                des = case.case_description
                gender, age = des.split(',')
                w1, w2 = age.split('(')
                w3, w4 = w2.split(')')
                begin, end = w3.split('-')
                age_begin = int(begin)
                age_end = int(end)
                age = (age_begin + age_end) / 2
                dicx['gender'] = gender
                dicx['age'] = age
                if 0 <= age < 18:
                    dic['0-18'] = dic['0-18'] + 1
                elif 18 <= age < 45:
                    dic['18-45'] = dic['18-45'] + 1
                elif 45 <= age < 65:
                    dic['45-65'] = dic['45-65'] + 1
                elif 65 <= age < 100:
                    dic['65-100'] = dic['65-100'] + 1

    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Empty Case"
        return HttpResponse(json.dumps(dic))

    return HttpResponse(json.dumps(dic))


#   一月内入侵人员性别统计（用户）
@csrf_exempt
def count_human_gender(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        user_id = post_content['id']
        user = User.objects.get(id=user_id)
        cameras = Camera.objects.filter(owner=user)
        dic['status'] = 'Success'
        dic['male'] = dic['female'] = 0
        for camera in cameras:
            now = timezone.now()
            start = now - datetime.timedelta(days=30)
            cases = Case.objects.filter(date_time__gte=start, case_type=2, detect_camera=camera)
            for case in cases:
                dicx = {}
                des = case.case_description
                gender, age = des.split(',')
                if gender == 'Male':
                    dic['male'] = dic['male'] + 1
                elif gender == 'Female':
                    dic['female'] = dic['female'] + 1
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Empty Case"
        return HttpResponse(json.dumps(dic))

    return HttpResponse(json.dumps(dic))


# 一周内每天入侵车和人情况
@csrf_exempt
def count_week_case(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        user_id = post_content['id']
        case = User.objects.get(id=user_id)
        cameras = Camera.objects.filter(owner=case)
        array = []
        for camera in cameras:
            now = timezone.now()
            start = now - datetime.timedelta(days=7)
            cases = Case.objects.filter(Q(date_time__gte=start, case_type=2, detect_camera=camera)
                                        | Q(date_time__gte=start, case_type=1, detect_camera=camera))
            disc = {'camera_id': camera.id, 'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0,
                    'saturday': 0, 'sunday': 0}
            for case in cases:
                day = case.date_time.weekday()  # 0-6 星期一到星期日
                if day == 0:
                    disc['monday'] = disc['monday'] + 1
                elif day == 1:
                    disc['tuesday'] = disc['tuesday'] + 1
                elif day == 2:
                    disc['wednesday'] = disc['wednesday'] + 1
                elif day == 3:
                    disc['thursday'] = disc['thursday'] + 1
                elif day == 4:
                    disc['friday'] = disc['friday'] + 1
                elif day == 5:
                    disc['saturday'] = disc['saturday'] + 1
                elif day == 6:
                    disc['sunday'] = disc['sunday'] + 1
            array.append(disc)
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Empty Case"
        return HttpResponse(json.dumps(dic))
    dic['status'] = 'Success'
    dic['case_list'] = array
    return HttpResponse(json.dumps(dic))


# 一周有四个的监控入侵情况
# 先查询用户的摄像头有几个，然后再查看各自摄像头的一周情况
@csrf_exempt
def count_week_camera(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        post_content = json.loads(request.body)
        user_id = post_content['id']
        user = User.objects.get(id=user_id)
        cameras = Camera.objects.filter(owner=user)

        dic['status'] = 'Success'
        dic['monday'] = dic['tuesday'] = dic['wednesday'] = dic['thursday'] = dic['friday'] = dic['saturday'] = dic[
            'sunday'] = 0
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
