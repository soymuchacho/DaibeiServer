#coding=utf-8
from django.db import models

# Create your models here.

class User(models.Model):
    # ID
    userid = models.IntegerField()
    # 用户名
    username = models.CharField(max_length=64)
    # 密码
    password = models.CharField(max_length=64)
    # 邮箱
    email = models.CharField(max_length=320)
    # 电话
    phone = models.CharField(max_length=64)
    # 职位
    position = models.IntegerField()
    # 生日
    birthday = models.CharField(max_length=64)
    # 性别
    sex = models.IntegerField()
    # 工号
    number = models.CharField(max_length=64)
    # 直属经理
    manager = models.CharField(max_length=64)
    # 入职时间
    entry_time = models.CharField(max_length=64)
    # Token
    token = models.CharField(max_length=64)
