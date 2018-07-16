#coding=utf-8
from django.db import models

class User_Info(models.Model):
	# 用户名(机器编码)
    username = models.CharField(max_length=64)
    # 机器外身编码
    username2 = models.CharField(max_length=64, default="")
    # 密码
    password = models.CharField(max_length=64)
    # 位置
    location = models.CharField(max_length=1024)
    # 管理人员 
    manager = models.CharField(max_length=64, default="")
    # 开始使用时间
    use_time = models.CharField(max_length=64)
    # 微信公众号类型
    wechatType = models.CharField(max_length=64, default="0")		# 0服务号  1订阅号
    # 微信公众号编码
    wechatNumber = models.CharField(max_length=64,default="")

    def __str__(self):
		return self.username

class Admin_Info(models.Model):
	# 用户名
	adminname = models.CharField(max_length=64)
	# 密码
	password = models.CharField(max_length=64)

	def __str__(self):
		return self.adminname
