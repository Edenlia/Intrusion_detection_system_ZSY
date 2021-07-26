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

    # last_login = models.TimeField(default=timezone.now())

    def __str__(self):
        return self.username


class Camera(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80)
    type = models.IntegerField()  # 0.正常情况（一般不会出现，占位用） 1.指定区域有人入侵 2.识别入侵人物脸部情况 3.指定区域车辆进入 4.识别车牌情况
    url = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user'
    )


class Case(models.Model):
    id = models.BigAutoField(primary_key=True)
    checked = models.BooleanField(default=0)
    case_type = models.IntegerField()  # 什么样的   0 1  2 3
    case_description = models.TextField()
    level = models.IntegerField()
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
