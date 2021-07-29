from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('log/login/', views.login, name='login'),
    path('log/register/', views.register, name='register'),
    path('log/change_password/', views.change_password, name='change_password'),
    path('log/add_admin/', views.add_admin, name='add_admin'),
    path('log/delete_account/', views.delete_account, name='delete_account'),
    path('log/query_all/', views.query_all, name='query_all'),
    path('log/query_user/', views.query_user, name='query_user'),

    path('camera/add_camera/', views.add_camera, name='add_camera'),
    path('camera/delete_camera/', views.delete_camera, name='delete_camera'),
    path('camera/change_url/', views.change_url, name='change_url'),
    path('camera/change_name/', views.change_name, name='change_name'),
    path('camera/query_camera_detail/', views.query_camera_detail, name='query_camera_detail'),
    path('camera/query_camera/', views.query_camera, name='query_camera'),

    path('case/add_case/',views.add_case),
    path('case/delete_case/', views.delete_case, name='delete_case'),
    path('case/change_checked/', views.change_checked, name='change_checked'),
    path('case/query_all_case/', views.query_all_case, name='query_all_case'),
    path('case/query_case/', views.query_case, name='query_case'),


    path('count/count_all/', views.count_all),
    path('count/count_user/',views.count_user),

    path('car/add_car_record/',views.add_car_record),
    path('car/delete_car_record/',views.delete_car_record),
    # path('live/<name>', views.live, name='live'),
]
