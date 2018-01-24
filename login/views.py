#coding:utf-8
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from .forms import LoginForm
from .RsaUtil import *
from django.core.cache import cache
from base.logger import *
from base.defines import *
import json
import time
import hashlib
import datetime
import sys
from login.models import User_Info
from login.models import Admin_Info
from login.sql import *
from .Authentication import *
from resourceManager.models import *
from dwebsocket import require_websocket 

token_secretkey = "1qaz@WSX3edc$RFV5tgb^YHN7ujm*IK<0p;/"


# 帐号注册
def Register(request):
	if request.method == 'POST':
		log_write('info','开始注册')
		username = request.POST.get('username')
		password = request.POST.get('password')
		location = request.POST.get('location')
		if username == None:
			log_write('info','用户名错误')
			return HttpResponse("{'error':'用户名错误'}")
		if password == None:
			log_write('info','密码错误')
			return HttpResponse("{'error':'密码错误'}")
		if location == None:
			log_write('info','位置信息错误')
			return HttpResponse("{'error':'位置信息错误'}")
		
		log_write('info','开始注册')
		bRet = RegisterUser(username,password,location)
		if bRet == False:
			log_write('info','账号注册失败')
			return HttpResponse("{'error':'账号注册失败'}")
		log_write('info','帐号注册成功')
		return HttpResponse("{'code':'200','msg' : 'ok'}")
	else:
		return HttpResponse("{'error' : 'request post '}")

# 帐号验证
def Authentication(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		log_write('info','账号认证')
		
		if username == None:
			return HttpResponse("{'error' : 'username error'}")
		
		if password == None:
			return HttpResponse("{'error' : 'password error'}")


		# 检测帐号
		user = User_Info.objects.filter(username=username)
		if len(user) == 0:
			return HttpResponse("{'error':'username or password error'}")
		
		if password == user[0].password:
			ret_dict = {}
			
			# 生成token
			result = GenerateToken(user[0].username,token_secretkey)
			ret_dict['token'] = result

			log_write('info','生成token : ')
			log_write('info',result)
			# 以username为key设置一个缓存，再以token为key设置一个token对应的username
			cache.set(result,username,ACCOUNT_LOGIN_DEFAULT_TIME)
			
			ret_json = json.dumps(ret_dict)
			return HttpResponse(ret_json)
		else:
			return HttpResponse("{'error':'username or password error'}")
	else:
		return HttpResponse("{'error':'badmethod'}") 


# 登陆界面
def AdminLogin(request):
    return render(request,'management/login.html')

# 管理员账号注册
def AdminRegister(request):
	if request.method == 'POST':
		log_write('info','开始注册')
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username == None:
			log_write('info','用户名错误')
			return HttpResponse("{'error':'用户名错误'}")
		if password == None:
			log_write('info','密码错误')
			return HttpResponse("{'error':'密码错误'}")
		
		log_write('info','开始注册')
		bRet = RegisterAdmin(username,password)	
		if bRet == False:
			return HttpResponse("{'error':'注册失败'}")
		log_write('info','帐号注册成功')
		return HttpResponse("{'code':'200','msg' : 'ok'}")
	else:
		return HttpResponse("{'error' : 'request post '}")
	return HttpResponse("{'error':'badmethod'}")



# 管理员账号登陆验证
def AdminAuthentication(request):
	if request.method == 'POST':
		log_write('info','管理员账号登陆')
		adminname = request.POST.get('username',None)
		password = request.POST.get('password',None)
		log_write('info','获取账号密码')
		if adminname == None:
			return HttpResponse("{'error':'用户名不存在'}")
		if password == None:
			return HttpResponse("{'error':'密码不存在'}")
		log_write('info','账号 密码开始验证')	
		
		# 进行认证
		adminuser = Admin_Info.objects.filter(adminname=adminname)
		if len(adminuser) == 0:
			return HttpResponse("{'error':'用户名或密码错误'}")
		log_write('info','用户存在')	
		if password == adminuser[0].password:
			result = {}
			token = GenerateToken(adminname,token_secretkey)
			log_write('info','generatetoken')
			log_write('info',token)
			# 以username为key设置一个缓存，再以token为key设置一个token对应的username
			cache.set(token,adminname,ACCOUNT_LOGIN_DEFAULT_TIME)
			
			result['token'] = token
			
			ret_json = json.dumps(result)
			log_write('info','render to response')
			return HttpResponse(ret_json)
		else:
			return HttpResponse("{'error':'用户名或密码错误'}")
	else:
		return HttpResponse("{'error':'badmethod'}")

# 登录成功，进入系统
def EnterManager(request):
	if request.method == 'GET':
		log_write('info','EnterManager')
		oauth = request.GET.get('next',None)
		if oauth == None:
			return render(request,'management/login.html')
		
		log_write('info','获取到oauth')
		user = CheckAdminToken(oauth)	
		if user == None:
			return render(request,'management/login.html')
		log_write('info','用户检测通过')

		username = user.adminname		
		return render(request,'management/index.html',{'username':username})

# 获取全部用户
def GetAllUserList(request):
	if request.method == 'GET':
		log_write('info','GetAllUserList')
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		admin = CheckAdminToken(oauth)
		if admin == None:
			log_write('info','can not find oauth')
			return HttpResponse("{'error':'oauth error'}")
	
		ret_dict = {}
		
		page = int(request.GET.get('page',0))
		if page == 0:
			return HttpResponse("{'error':'page error'}")
		
		userlist = GetAllUserListFromSQL(page);
		if userlist != None:
			ret_dict['count'] = GetAllUserListNum()
			ret_dict['pages'] = GetAllUserListPageCount()
			ret_dict['users'] = []
			
			log_write('indo','userlist')
			for user in userlist:
				node = {}
				node['username'] = user.username
				node['location'] = user.location
				
				# 查找resourceManager中的UserResourceList表
				res_info = UserResourceList.objects.filter(username=user.username)
				if len(res_info) != 0:
					version = res_info[0].list_version
				else:
					version = ""
				node['version'] = version
				date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				node['date'] = user.use_time 
				ret_dict['users'].append(node)
				log_write('info',user.username)
				log_write('info',user.location)
				log_write('info',version)
				log_write('info',date)
			ret_json = json.dumps(ret_dict)
			log_write('info',ret_json)
			return HttpResponse(ret_json)		
		log_write('info','no userlist')	
		return HttpResponse("{}")


@require_websocket
def WebSocketConnect(request):
	message = request.websocket.wait()
	request.websocket.send(message)	

