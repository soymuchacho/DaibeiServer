# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class WeiXinUser(models.Model):
	# 微信账户
	weixinAccount = models.CharField(max_length=256)
	# 微信用户的APPID
	weixinAppID = models.CharField(max_length=256)
	# 游戏次数
	gametimes = models.IntegerField()

	def __str__(self):
		return self.weixinAccount
