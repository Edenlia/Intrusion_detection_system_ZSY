from django.db import models
from PIL import Image
from django.core.files import File
from datetime import datetime
from io import BytesIO
from django.utils import timezone


# user id permission username password
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    permission = models.IntegerField(default=0)  # user is 0 ,admin=1
    username = models.CharField(max_length=30)
    password = models.TextField()
    date_time = models.DateTimeField(default=timezone.now())

    # 注册时间,默认

    # last_login = models.TimeField(default=timezone.now())

    def __str__(self):
        return self.username


class Camera(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80)
    type = models.IntegerField()  # 0.正常情况（一般不会出现，占位用） 1.区域熟人进入 2.普通区域陌生人入侵，脸部情况  3.车辆进入识别车牌 4.危险区域人员入侵
    url = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user'
    )


class Case(models.Model):
    id = models.BigAutoField(primary_key=True)
    checked = models.BooleanField(default=0)
    case_type = models.IntegerField()  # 什么样的  0 1.区域熟人进入 2.普通区域陌生人入侵，脸部情况  3.车辆进入识别车牌 4.危险区域人员入侵

    case_description = models.TextField()  # 描述信息
    level = models.IntegerField()
    # 1.人员0-18  2.车辆 3.人员45 -65 4.人员18-45 5.危险区域
    date_time = models.DateTimeField(default=timezone.now())
    img = models.TextField()  # base64图片文件,包含前缀
    # img = models.ImageField(upload_to='img')
    detect_camera = models.ForeignKey(
        Camera, on_delete=models.CASCADE, related_name='camera'
    )


class Car_Record(models.Model):
    id = models.BigAutoField(primary_key=True)
    car_brand = models.TextField()
# Create your models here.
