from django.urls import path

from . import views

urlpatterns = [
     path('test1', views.test1, name='live1'),
     path('test2', views.test2, name='live2'),
     path('test3', views.test3, name='live3')
]