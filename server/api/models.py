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
    tap = models.IntegerField()  # 0 1.车牌 2.人脸 3.移动物体 4.
    url = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user'
    )
    description = models.TextField()


class Case(models.Model):
    id = models.BigAutoField(primary_key=True)
    detect_camera = models.ForeignKey(
        Camera, on_delete=models.CASCADE, related_name='camera'
    )
    checked = models.BooleanField(default=0)
    case_type = models.IntegerField()  # 什么样的
    case_description = models.TextField()
    level = models.IntegerField()
    date_time = models.DateField(default=timezone.now())
    img = models.ImageField(upload_to='img')


class Car_Record(models.Model):
    id = models.BigAutoField(primary_key=True)
    car_brand = models.TextField()
# Create your models here.
