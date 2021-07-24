from django.urls import path

from . import views

urlpatterns = [
    path('log/login/', views.login, name='login'),
    path('log/register/', views.register, name='register'),
    path('log/change_password/', views.change_password, name='change_password'),
    path('log/add_admin/', views.add_admin, name='add_admin'),
    path('log/delete_account/',views.delete_account,name='delete_account'),
    path('log/query_all/',views.query_all,name='query_all'),
    path('log/query_user/',views.query_user,name='query_user'),

    path('camera/add_camera/',views.add_camera,name='add_camera'),
    path('camera/delete_camera/',views.delete_camera,name='delete_camera'),
    path('camera/change_url/',views.change_url,name='change_url'),
]
