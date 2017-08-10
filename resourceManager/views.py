# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resourceManager.models import *
from django.shortcuts import render
from django.http import HttpResponse
from base.logger import *
from .upload import *
from .download import *
from django.core.cache import cache
import os
from login.Authentication import * 
from .resource import *

####################################################################################
#																				   #
#							用户账号操作										   #
#																				   #
####################################################################################

# 获取用户资源列表版本
def GetUserResourceListVersion(request):
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		log_write('info','get user resource list version oauth %s',oauth)
		# 认证
		user = CheckUserToken(oauth)
		if user == None:
			return HttpResponse("{'error':'bad user'}")

		result = GetResourceListVersion(user)
		if result == None:
			return HttpResponse("{'error' : 'get version error'}")
		
		return HttpResponse(result)
	else:
		return HttpResponse("{'error' : 'badmethod'}")

# 获取用户资源列表
def GetUserResourceList(request):
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		# 进行认证
		user = CheckUserToken(oauth)
		if user == None:
			return HttpResponse("{'error':'bad user'}")
		
		# 从数据库中获取资源列表
		result = GetResourceList(user)
		if result == None:
			return HttpResponse("{'error':'can't find resource list'}")

		return HttpResponse(result)
	else:
		return HttpResponse("{'error':'badmethod'}")

# 资源下载
def Download_Resource(request):
	if request.method == 'GET':
		#oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		# 进行认证
		#user = CheckUserToken(oauth)
		#if user == None:
		#	return HttpResponse("{'error':'bad user'}")

		fileid = request.GET.get('fileid')
		print request.POST
		log_write('info','download file id %s',fileid)
		response = ResourceDownLoad(fileid)
		if response == None:
			return HttpResponse("{'error':'bad fileid'}")
		
		return response
	else:
		return HttpResponse("{'error':'badmethod'}")

####################################################################################
#																				   #
#							管理员账号操作										   #
#																				   #
####################################################################################
	
	
def uploadhtml(request):
	return render(request,'upload.html')

# 资源上传
def Upload_Resource(request):
	if request.method == 'POST':
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		# 进行认证
		user = CheckAdminToken(oauth)
		#if user == None:
		#	return HttpResponse("{'error':'bad user'}")
		
		fileid = request.POST.get('id',None)
		if not fileid:
			return HttpResponse("{'error' : 'no files id'}")
		
		uploadSize = request.POST.get('size',None)				# 上传文件的大小
		if not uploadSize:
			return HttpResponse("{'error' : 'no files size'}")
		
		restype = request.POST.get('type',None)				# 上传文件的类型
		if not restype:
			return HttpResponse("{'error' : 'no files type'}")

		resdesc = request.POST.get('desc',None)				# 上传文件的描述
		if not resdesc:
			return HttpResponse("{'error' : 'no files description'}")

		uploadFile = request.FILES.get('file',None)				# 获取上传的文件，如果没有文件，则默认为None
		if not uploadFile:
			return HttpResponse("{'error' : 'no files for upload'}")
		
		log_write('info','upload file : %s %s %s',uploadFile.name,user,fileid)	
	
		filepath = os.path.join("/root/Resource",uploadFile.name)
		dest = open(filepath,'wb+')
		# 文件大于2.5M时，分片读取，否则直接读取
		if uploadFile.multiple_chunks() == False:
			content = uploadFile.read()
			dest.write(content)
		else:
			for chunk in uploadFile.chunks():
				dest.write(chunk)
		dest.close()

		totalsize = os.path.getsize(filepath)
		log_write('info','upload size %s,total size %d',uploadSize,totalsize)
		
		if totalsize != long(uploadSize):
			# 将现有的文件删除
			os.remove(filepath)
			return HttpResponse("{'error' : 'upload file failed,not all size'}")
		
		# 将上传的文件信息保存在数据库中
		SaveResourceToSQL(fileid,uploadFile.name,filepath,uploadSize,restype,resdesc)	
		
		log_write('info','upload file : %s successful!!',uploadFile.name)	
		return HttpResponse("{'msg':'upload ok'}")
	else:
		return HttpResponse("{'error':'badmethod'}")


# 资源删除
def Delete_Resource(request):
	if request.method == 'POST':
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		# 进行认证
		user = CheckAdminToken(oauth)
		if user == None:
			return HttpResponse("{'error':'bad user'}")
	else:
		return HttpResponse("{'error':'badmethod'}")


# 设置用户资源列表
def ResetUserResourceList(request):
	return HttpResponse("{'error':'badmethod'}")

