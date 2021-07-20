# Generated by Django 3.2.5 on 2021-07-20 06:18

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('checked', models.BooleanField(default=0)),
                ('checked_admin', models.IntegerField(default=-1)),
                ('date_time', models.DateField(default=datetime.datetime(2021, 7, 20, 6, 18, 15, 908799, tzinfo=utc))),
                ('img', models.ImageField(upload_to='img')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('permission', models.IntegerField(default=0)),
                ('username', models.CharField(max_length=30)),
                ('password', models.TextField()),
                ('last_login', models.TimeField(default=datetime.datetime(2021, 7, 20, 6, 18, 15, 908799, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='User_Camera_Relation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('camera_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='camera', to='api.camera')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to='api.user')),
            ],
        ),
    ]
