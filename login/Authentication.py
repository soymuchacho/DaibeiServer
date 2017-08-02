#coding=utf-8

from django.core.cache import cache
from login.models import *
from base.logger import *

# 验证token并返回username
def CheckToken(token):
	log_write('info','check token %s',token)
	username = cache.get(token)
	if username == None:
		# 缓存中不存在...从数据库中直接查找
		user = User_Info.filter.get(token=token)
		if len(user) == 0:
			# 数据库中也不存在
			log_write('info','check token %s failed!',token)
			return None
		username = user.username
		# 保存到缓存中
		cache.set(token,username,0)

	user = cache.get(username)
	if user == None:
		# 缓存中不存在...从数据库中查找
		user = User_Info.filter.get(username=username)
		if len(user) == 0:
			#数据库中也不存在，返回None
			log_write('info','check token %s failed!',token)
			return None
		# 保存到缓存中
		cache.set(username,user,0)
	
	log_write('info','check token %s successful! username %s',token,user.username)
	return user
