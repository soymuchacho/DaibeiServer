#coding=utf-8
import time
import json
import hashlib
from django.core.cache import cache
from login.models import *
from base.logger import *
from .RsaUtil import *
from base.defines import *


ACCOUNT_LOGIN_DEFAULT_TIME = 24 * 60 * 60

def GenerateToken(username,token_secretkey):
	log_write('info','开始生成token')
	# 生成token md5(base64(用户名+密钥+当前时间))
	now_time = time.strftime("%Y-%02m-%02d %02H:%02M:%02S",time.localtime(time.time()))
	encode_str = Base64Encode(username+token_secretkey+now_time)
	m2 = hashlib.md5()
	m2.update(encode_str)
	token = m2.hexdigest().encode('utf-8')
	log_write('info','生成token')
	log_write('info',token)
	return token

def RegisterUser(username,password,location):
	# 先查询数据库用户是否已经存在
	old_user = User_Info.objects.filter(username=username)
	if len(old_user) != 0:
		#log_write('info','用户%s已存在,注册失败',username)
		return False

	old_admin = Admin_Info.objects.filter(adminname=username)
	if len(old_admin) != 0:
		#log_write('info','用户%s已存在,注册失败',username)
		return False
	log_write('info','用户不存在，可以注册')
	
	now_time = time.strftime("%Y-%02m-%02d %02H:%02M:%02S",time.localtime(time.time()))
	
	# 用户不存在，创建
	new_user = User_Info(username=username,password=password,location=location,use_time=now_time)
	if new_user == None:
		return False
	new_user.save()
	return True

def RegisterAdmin(username,password):
	# 先查询数据库用户是否已经存在
	old_user = User_Info.objects.filter(username=username)
	if len(old_user) != 0:
		#log_write('info','用户%s已存在,注册失败',username)
		return False

	old_admin = Admin_Info.objects.filter(adminname=username)
	if len(old_admin) != 0:
		#log_write('info','用户%s已存在,注册失败',username)
		return False
	log_write('info','用户不存在，可以注册')
	
	# 用户不存在，创建
	new_user = Admin_Info(username=username,password=password)
	if new_user == None:
		return False
	new_user.save()
	return True


# 验证token并返回username
def CheckUserToken(token):
	log_write('info','check token')
	log_write('info',token)
	username = cache.get(token)
	if username == None:
		log_write('info','username is None')
		#log_write('info','check token %s failed!',token)
		return None

	# 缓存中不存在...从数据库中查找
	user = User_Info.objects.filter(username=username)
	if len(user) == 0:
		#数据库中也不存在，返回None
		#log_write('info','check token %s failed!',token)
		return None
	user = user[0]
	return user

# 验证管理员账号token并返回adminname
def CheckAdminToken(token):
	log_write('info','check admin token ')
	log_write('info',token)
	adminname = cache.get(token)
	if adminname == None:
		# 缓存中不存在，从数据库中查找
		#log_write('info','check admin token %s failed!',token)
		return None
	
	admin = Admin_Info.objects.filter(adminname=adminname)
	if len(admin) == 0:
		# 数据库中不存在，返回None
		log_write('info','check admin token failed!')
		return None
	# 保存到缓存中
	admin = admin[0]

	log_write('info','check admin token successful! ')
	return admin


