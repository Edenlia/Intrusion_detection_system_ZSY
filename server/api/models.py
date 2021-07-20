from django.db import models
from django.db import models
from PIL import Image
from django.core.files import File
from datetime import datetime
from io import BytesIO
from django.utils import timezone


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    permission = models.IntegerField(default=0)  # user is 0 ,admin=1
    username = models.CharField(max_length=30)
    password = models.TextField()
    # last_login = models.TimeField(default=timezone.now())

    def __str__(self):
        return self.username


class Log(models.Model):
    id = models.BigAutoField(primary_key=True)
    checked = models.BooleanField(default=0)
    checked_admin = models.IntegerField(default=-1)
    date_time = models.DateField(default=timezone.now())
    img = models.ImageField(upload_to='img')


class Camera(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.TextField()


class User_Camera_Relation(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='user'
    )
    camera_id = models.ForeignKey(
        Camera, on_delete=models.DO_NOTHING, related_name='camera'
    )

# Create your models here.
