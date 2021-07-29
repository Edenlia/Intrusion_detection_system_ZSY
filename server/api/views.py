import threading

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.views.decorators import gzip
from django.views.decorators.csrf import csrf_exempt

import json
import datetime
from django.utils import timezone
# 导入model中的User
from .models import User, Camera, Case, Car_Record

# 代码编码规则
# 下划线命名法
# 函数名 动作+对象，如更改密码 change——password

import base64
import cv2

# video_cameras = []
import cv2
import numpy as np
from qiniu import Auth, put_file, etag
import qiniu.config

ak = 'gllUD3Ik4X7BaXw44GBY6jKfqI9K5qLhNCFZ7uf8'
sk = 'La3cQhn95ATO4pACyogVtHWxeFvkLejMEwHh1vVv'
bn = 'intrusion-detection-system'


def send_img_to_server(AK, SK, BUCKET_NAME, KEY, DATA):
    # 构建鉴权对象
    q = Auth(AK, SK)
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(BUCKET_NAME, KEY, 3600)
    # 要上传文件的本地路径
    ret, info = put_file(token, KEY, DATA, version='v2')


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
        if len(camera) != 0:
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
        users = User.objects.all()
        array = []
        for user in users:
            cameras = Camera.objects.filter(owner=user)
            dics = {'id': user.id, "username": user.username,
                    "permission": user.permission, "date_time": user.date_time,
                    "camera_num": len(cameras)}
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
    return HttpResponse(json.dumps(dic, cls=DateEncoder))


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
        if len(cameras) != 0:
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
# 用户通过摄像头id查询摄像头详细信息
# id
@csrf_exempt
def query_camera_detail(request):
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


@csrf_exempt
def query_camera(request):
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
        dic['camera_list'] = []
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except User.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong User Id"
        return HttpResponse(json.dumps(dic))
    except Camera.DoesNotExist:
        dic['status'] = "Success"
        dic['message'] = "No Camera"
        return HttpResponse(json.dumps(dic))
    dic['status'] = "Success"
    for camera in cameras:
        cam = {'name': camera.name, 'id': camera.id, 'url': camera.url, 'type': camera.type,
               'description': camera.description}
        dic['camera_list'].append(cam)
    return HttpResponse(json.dumps(dic))


# 增加异常
# 传入case_type和case_description
@csrf_exempt
def add_case(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))

    try:
        # print("run in")
        post_content = json.loads(request.body)
        case_type = post_content['case_type']
        case_description = post_content['case_description']
        img = post_content['img']
        detect_camera_id = post_content['detect_camera_id']
        camera = Camera.objects.get(id=detect_camera_id)
        if case_type == 1:
            car_record = Car_Record.objects.get(car_brand=case_description)
            # 首先查找不是记录的摄像头，然后异常里面再添加异常
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))

    except Car_Record.DoesNotExist:
        dic['status'] = 'Failed'
        if case_type == 1:
            # 上传图片
            key = case_description + '.jpg'
            send_img_to_server(ak, sk, bn, key, img)
            # http: // ids.edenlia.icu / img_error.jpg
            img = "http://ids.edenlia.icu/" + key
            # 添加异常
            new_case = Case(case_type=case_type, case_description=case_description, level=3, img=img,
                            detect_camera=camera)
            new_case.save()
        dic['message'] = 'Add Car_case'
        return HttpResponse(json.dumps(dic))
    except Camera.DoesNotExist:
        dic['status'] = 'Failed'
        dic['message'] = 'Wrong Camera_id'

    dic['status'] = "Success"
    return HttpResponse(json.dumps(dic))


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


# 查询所有的异常信息
# 用户id
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
        if len(cameras) != 0:
            for camera in cameras:
                cases = Case.objects.filter(detect_camera=camera).order_by('-date_time')  # 按时间排序
                if len(cases) != 0:
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
        dic['description'] = case.case_description
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
        return HttpResponse(json.dumps(dic))

    return HttpResponse(json.dumps(dic, cls=DateEncoder))


# 统计一个月早中晚入侵人数和车
# 查询数据库中一个月的内容
@csrf_exempt
def count_all(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:

        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=30)
        array = []
        for i in range(2):
            dis = {'morning': 0, 'noon': 0, 'evening': 0}
            cases = Case.objects.filter(date_time__gte=start, case_type=i + 1)
            for case in cases:
                dicx = case.date_time.strftime('%H')
                hour = int(dicx)
                if 0 <= hour < 4:
                    dis['evening'] = dis['evening'] + 1
                elif 4 <= hour < 11:
                    dis['morning'] = dis['morning'] + 1
                elif 11 <= hour < 18:
                    dis['noon'] = dis['noon'] + 1
                else:
                    dis['evening'] = dis['evening'] + 1
            array.append(dis)

        start2 = now - datetime.timedelta(days=7)
        users2 = User.objects.filter(date_time__gte=start2)

        # 近一周每天的所有异常
        # 遍历所有不为3的异常
        dism = {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0,
                'saturday': 0, 'sunday': 0}
        for i in range(2):
            cases = Case.objects.filter(date_time__gte=start, case_type=i + 1)
            for case in cases:
                # 筛选星期
                day = case.date_time.weekday()
                if day == 0:
                    dism['monday'] = dism['monday'] + 1
                elif day == 1:
                    dism['tuesday'] = dism['tuesday'] + 1
                elif day == 2:
                    dism['wednesday'] = dism['wednesday'] + 1
                elif day == 3:
                    dism['thursday'] = dism['thursday'] + 1
                elif day == 4:
                    dism['friday'] = dism['friday'] + 1
                elif day == 5:
                    dism['saturday'] = dism['saturday'] + 1
                elif day == 6:
                    dism['sunday'] = dism['sunday'] + 1

        # 近一周每天注册人数
        array2 = []
        disc = {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0,
                'saturday': 0, 'sunday': 0}
        for user in users2:
            day = user.date_time.weekday()  # 0-6 星期一到星期日
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
        array2.append(disc)


    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Empty Case"
        return HttpResponse(json.dumps(dic))

    dic['status'] = 'Successes'
    dic['case_list'] = array  # 30天入侵统计
    dic['case_week'] = dism  # 近一周入侵的人
    dic['register_list'] = array2  # 近一周新注册人数
    return HttpResponse(json.dumps(dic))


# 实现一周 四个摄像头情况和合起来情况
@csrf_exempt
def count_user(request):
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
        dicx = {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0,
                'saturday': 0, 'sunday': 0}
        dics = {'male': 0, 'female': 0, 'e0_18': 0, 'e18_45': 0, 'e45_65': 0, 'e65_100': 0}
        for camera in cameras:
            now = timezone.now()
            start = now - datetime.timedelta(days=7)
            cases = Case.objects.filter(Q(date_time__gte=start, case_type=2, detect_camera=camera)
                                        | Q(date_time__gte=start, case_type=1, detect_camera=camera))
            disc = {'camera_name': camera.name, 'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0,
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
            dicx['monday'] = dicx['monday'] + disc['monday']
            dicx['tuesday'] = dicx['tuesday'] + disc['tuesday']
            dicx['wednesday'] = dicx['wednesday'] + disc['wednesday']
            dicx['thursday'] = dicx['thursday'] + disc['thursday']
            dicx['friday'] = dicx['friday'] + disc['friday']
            dicx['saturday'] = dicx['saturday'] + disc['saturday']
            dicx['sunday'] = dicx['sunday'] + disc['sunday']

            start2 = now - datetime.timedelta(days=30)
            cases2 = Case.objects.filter(date_time__gte=start, case_type=2, detect_camera_id=camera)
            for case in cases2:
                des = case.case_description
                gender, age = des.split(',')
                if gender == 'Male':
                    dics['male'] = dics['male'] + 1
                elif gender == 'Female':
                    dics['female'] = dics['female'] + 1
                w1, w2 = age.split('(')
                w3, w4 = w2.split(')')
                begin, end = w3.split('-')
                age_begin = int(begin)
                age_end = int(end)
                age = (age_begin + age_end) / 2
                if 0 <= age < 18:
                    dics['e0_18'] = dics['e0_18'] + 1
                elif 18 <= age < 45:
                    dics['e18_45'] = dics['e18_45'] + 1
                elif 45 <= age < 65:
                    dics['e45_65'] = dics['e45_65'] + 1
                elif 65 <= age < 100:
                    dics['e65_100'] = dics['e65_100'] + 1


    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Case.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Empty Case"
        return HttpResponse(json.dumps(dic))
    dic['status'] = 'Success'
    dic['case_month'] = dics
    dic['case'] = dicx
    dic['case_list'] = array
    return HttpResponse(json.dumps(dic))


# 添加车牌
# 传入车牌号 car_brand
@csrf_exempt
def add_car_record(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        car_brand = post_content['car_brand']
        car_record = Car_Record.objects.get(car_brand=car_brand)
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Car_Record.DoesNotExist:
        dic['status'] = "Success"
        # 添加车牌
        new_car_record = Car_Record(car_brand=car_brand)
        new_car_record.save()
        return HttpResponse(json.dumps(dic))

    dic['status'] = "Failed"
    dic['message'] = 'Car_record Exist'
    return HttpResponse(json.dumps(dic))


# 删除车牌
@csrf_exempt
def delete_car_record(request):
    dic = {}
    if request.method != 'POST':
        dic['status'] = "Failed"
        dic['message'] = "Wrong Method"
        return HttpResponse(json.dumps(dic))
    try:
        post_content = json.loads(request.body)
        car_record_id = post_content['id']
        car_record = Car_Record.objects.get(id=car_record_id)
        car_record.delete()
    except(KeyError, json.decoder.JSONDecodeError):
        dic['status'] = "Failed"
        dic['message'] = "No Input"
        return HttpResponse(json.dumps(dic))
    except Car_Record.DoesNotExist:
        dic['status'] = "Failed"
        dic['message'] = "Wrong Id"
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

# def start_camera(url):
#     camera = Camera.objects.get(url=url)
#     for video_camera in video_cameras:
#         if camera.name == video_camera.name:
#             return
#     cam = VideoCamera(camera.url, camera.name, camera.type)
#     video_cameras.append(cam)


# class VideoCamera(object):
#     def __init__(self, url):
#
#         self.video = cv2.VideoCapture(url)
#         (self.grabbed, self.frame) = self.video.read()
#         threading.Thread(target=self.licence_check(), args=()).start()
#         # if self.type == 1:
#         #     print("thread start")
#         #
#         # elif self.type == 2:
#         #     threading.Thread(target=self.human_face_check(), args=()).start()
#         # else:
#         #     threading.Thread(target=self.area_check(), args=()).start()
#
#     def __del__(self):
#         self.video.release()
#
#     def get_frame(self):
#         image = self.frame
#         _, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()
#
#     def licence_check(self):
#         try:
#             while True:
#                 (self.grabbed, self.frame) = self.video.read()
#         except BaseException:
#             print("error")
#
#     # def human_face_check(self):
#     #     try:
#     #         while True:
#     #             (self.grabbed, self.frame) = self.video.read()
#     #     except BaseException:
#     #         print("error")
#     #
#     # def area_check(self):
#     #     try:
#     #         while True:
#     #             (self.grabbed, self.frame) = self.video.read()
#     #     except BaseException:
#     #         print("error")
#
#
# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#
#
# @gzip.gzip_page
# @csrf_exempt
# def live(request, name):
#     try:
#         # camera = Camera.objects.get(name=name)
#         # print("url: " + camera.url)
#         cam = VideoCamera('rtmp://localhost:1935/live/home')
#         return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
#     except Camera.DoesNotExist:  # This is bad! replace it with proper handling
#         return HttpResponseRedirect('http://ids.edenlia.icu/img_error.jpg')
#     except BaseException:
#         pass


# camera = None
# for video_camera in video_cameras:
#     if video_camera.name is name:
#         camera = video_camera
#         break
# if camera is None:
#     try:
#         camera = Camera.objects.get(name=name)
#         vc = VideoCamera(camera.url, camera.name, camera.type)
#         video_cameras.append(vc)
#     except Camera.DoesNotExist:
#         return HttpResponseRedirect('http://ids.edenlia.icu/img_error.jpg')
#
# else:
#     return StreamingHttpResponse(gen(camera), content_type="multipart/x-mixed-replace;boundary=frame")
