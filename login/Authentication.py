#coding=utf-8

from django.core.cache import cache
from login.models import *
from base.logger import *

# 验证token并返回username
def CheckUserToken(token):
	log_write('info','check token %s',token)
	username = cache.get(token)
	if username == None:
		log_write('info','username is None')
		# 缓存中不存在...从数据库中直接查找
		user = User_Info.objects.filter(token=token)
		log_write('info','从数据库中获取用户数量 %d',len(user))
		if len(user) == 0:
			# 数据库中也不存在
			log_write('info','check token %s failed!',token)
			return None
		username = user[0].username
		log_write('info','find username from sql %s',username)
		# 保存到缓存中
		cache.set(token,username,0)

	user = cache.get(username)
	if user == None:
		# 缓存中不存在...从数据库中查找
		user = User_Info.objects.filter(username=username)
		if len(user) == 0:
			#数据库中也不存在，返回None
			log_write('info','check token %s failed!',token)
			return None
		# 保存到缓存中
		cache.set(username,user[0],0)
		user = user[0]

	log_write('info','check token %s successful! username %s',token,user.username)
	return user

# 验证管理员账号token并返回adminname
def CheckAdminToken(token):
	log_write('info','check admin token %s',token)
	adminname = cache.get(token)
	if adminname == None:
		# 缓存中不存在，从数据库中查找
		admin = Admin_Info.objects.filter(token=token)
		if len(admin) == 0:
			# 数据库中也不存在
			log_write('info','check admin token %s failed!',token)
			return None
		adminname = admin[0].adminname
		# 保存到缓存中
		cache.set(token,adminname,0)
	
	admin = cache.get(adminname)
	if admin == None:
		# 缓存中不存在，从数据库中查找
		admin = Admin_Info.objects.filter(adminname=adminname)
		if len(admin) == 0:
			# 数据库中不存在，返回None
			log_write('info','check admin token %s failed!',token)
			return None
		# 保存到缓存中
		cache.set(adminname,admin[0],0)
		admin = admin[0]

	log_write('info','check admin token %s successful! adminname %s',token,admin.adminname)
	return admin


