from django.urls import path

from . import views

urlpatterns = [
    path('log/login/', views.login, name='login'),
    path('log/register/', views.register, name='register'),
    path('log/change_password/', views.change_password, name='change_password'),
]
