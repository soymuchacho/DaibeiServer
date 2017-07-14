#coding=utf-8
from django.db import models

class User_Info(models.Model):
    # 用户名
    username = models.CharField(max_length=64)
    # 密码
    password = models.CharField(max_length=64)
    # 位置
    location = models.CharField(max_length=1024)
    # 管理人员 
    manager = models.CharField(max_length=64)
    # 开始使用时间
    use_time = models.CharField(max_length=64)
    # Token
    token = models.CharField(max_length=64)
    # 私钥
    privtekey = models.CharField(max_length=1024)
    # 公钥
    publickey = models.CharField(max_length=1024)
