# Intrusion_detection_system_ZSY


## 简单的使用方法：
后端启动方法：终端进入server文件夹，py manage.py runserver
创建超级管理员账号,py manage.py createsuperuser
数据库生成，生成数据库定义语言，py manage.py makemigrations,生成本地数据库，py manage.py migrate

每次model.py 更新后都需要进行数据库更新,需要删除数据库
setting.py 也需要更新数据库内容