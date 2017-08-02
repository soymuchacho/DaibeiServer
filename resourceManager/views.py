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
from login.Authentication import CheckToken

def uploadhtml(request):
	return render(request,'upload.html')

# 资源上传
def Upload_Resource(request):
	if request.method == 'POST':
		user = request.POST.get('user',None)
		if not user:
			return HttpResponse("{'error' : 'no user'}")
		
		fileid = request.POST.get('id',None)
		if not fileid:
			return HttpResponse("{'error' : 'no files id'}")
		
		uploadFile = request.FILES.get('file',None)				# 获取上传的文件，如果没有文件，则默认为None
		if not uploadFile:
			return HttpResponse("{'error' : 'no files for upload'}")
		
		log_write('info','upload file : %s %s %s',uploadFile.name,user,fileid)	
		
		dest = open(os.path.join("/root/Resource",uploadFile.name),'wb+')
		# 文件大于2.5M时，分片读取，否则直接读取
		if uploadFile.multiple_chunks() == False:
			content = uploadFile.read()
			dest.write(content)
		else:
			for chunk in uploadFile.chunks():
				dest.write(chunk)
		dest.close()
		log_write('info','upload file : %s successful!!',uploadFile.name)	
		return HttpResponse("{'msg':'upload ok'}")
	else:
		return HttpResponse("{'error':'badmethod'}")



# 资源下载
def Download_Resource(request):
	if request.method == 'POST':
		oauth = request.META.get('Authentication','unkown')
		# 进行认证
		CheckToken(oauth)

		fileid = request.POST.get('fileid')
		response = DownloadResource(fileid)
		if response == None:
			return HttpResponse("{'error':'bad fileid'}")
		return response
	else:
		return HttpResponse("{'error':'badmethod'}")
	

# 资源删除
def Delete_Resource(request):
	if request.method == 'POST':
		
	else:
		return HttpResponse("{'error':'badmethod'}")
