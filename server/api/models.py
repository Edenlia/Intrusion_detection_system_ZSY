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
    type = models.IntegerField()  # case type 1 未知车辆闯入 case type 2 未知人员闯入 case type 3 敏感区域有人闯入
    url = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user'
    )


class Case(models.Model):
    id = models.BigAutoField(primary_key=True)
    checked = models.BooleanField(default=0)
    case_type = models.IntegerField()   # case type 1 未知车辆闯入 case type 2 未知人员闯入 case type 3 敏感区域有人闯入
    case_description = models.TextField()  # 描述信息
    level = models.IntegerField()
    date_time = models.DateTimeField(default=datetime.now())
    img = models.TextField()  # url
    # img = models.ImageField(upload_to='img')
    detect_camera = models.ForeignKey(
        Camera, on_delete=models.CASCADE, related_name='camera'
    )


class Car_Record(models.Model):
    id = models.BigAutoField(primary_key=True)
    car_brand = models.TextField()
# Create your models here.
