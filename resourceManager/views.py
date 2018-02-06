#coding=utf-8 
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
from base.config_xml import *

####################################################################################
#																				   #
#							用户账号操作										   #
#																				   #
####################################################################################

# 获取用户资源列表版本
def GetUserResourceListVersion(request):
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		# 认证
		user = CheckUserToken(oauth)
		if user == None:
			return HttpResponse("{\"error\":\"bad user\"}")

		result = GetResourceListVersion(user)
		if result == None:
			return HttpResponse("{\"error\" : \"no version\"}")
		
		return HttpResponse(result)
	else:
		return HttpResponse("{\"error\" : \"badmethod\"}")

# 获取用户资源列表
def GetUserResourceList(request):
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		# 进行认证
		user = CheckUserToken(oauth)
		if user == None:
			return HttpResponse("{\"error\":\"bad user\"}")
		
		# 从数据库中获取资源列表
		result = GetResourceList(user)
		if result == None:
			return HttpResponse("{\"error\":\"can't find resource list\"}")

		return HttpResponse(result)
	else:
		return HttpResponse("{\"error\":\"badmethod\"}")

# 资源下载
def Download_Resource(request):
	if request.method == 'POST':
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		# 进行认证
		user = CheckUserToken(oauth)
		if user == None:
			return HttpResponse("{\"error\":\"bad user\"}")

		fileid = request.POST.get('fileid')
		print request.POST
		#log_write('info','download file id %s',fileid)
		response = ResourceDownLoad(fileid)
		if response == None:
			return HttpResponse("{\"error\":\"file is not exists\"}")
		
		return response
	else:
		return HttpResponse("{\"error\":\"badmethod\"}")

####################################################################################
#																				   #
#							管理员账号操作										   #
#																				   #
####################################################################################
	
	
def uploadhtml(request):
	return render(request,'upload.html')

# 获取全部资源
def GetAllResource(request):
	if request.method == 'GET':
		log_write('info','获取全部资源')
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		admin = CheckAdminToken(oauth)
		if admin == None:
			return HttpResponse("{\"error\":\"bad user\"}")
		
		page = int(request.GET.get('page',0))
		if page == 0:
			return HttpResponse("{\"error\",\"page error\"}")
		
		ret_dict = {}
		reslist = GetAllResourceFromSQL(page)
		if reslist != None:
			ret_dict["pages"] = GetAllResourcePageCount()
			ret_dict["resources"] = []
			for res in reslist:
				node = {}
				node["id"] = res.resource_id
				node["name"] = res.resource_name
				node["size"] = str(res.resource_size)
				node["type"] = res.resource_type
				node["desc"] = res.resource_describe
				node["date"] = res.resource_date
				ret_dict["resources"].append(node)
			ret_json = json.dumps(ret_dict)
			return HttpResponse(ret_json)
		else:
			return HttpResponse("{}")
	else:
		return HttpResponse("{\"error\":\"bad method\"}")
# 资源上传
def Upload_Resource(request):
	if request.method == 'POST':
		log_write('info','upload resource')
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		# 进行认证
		user = CheckAdminToken(oauth)
		if user == None:
			return HttpResponse("{\"error\":\"bad user\"}")
		
		uploadSize = request.POST.get('size',None)				# 上传文件的大小
		strs = 'uploadSize %s' % uploadSize
		log_write('info',strs)
		if uploadSize == None:
			return HttpResponse("{\"error\" : \"no files size\"}")
		
		restype = request.POST.get('type',None)				# 上传文件的类型
		if not restype:
			return HttpResponse("{\"error\" : \"no files type\"}")

		resdesc = request.POST.get('desc',None)				# 上传文件的描述
		if not resdesc:
			return HttpResponse("{\"error\" : \"no files description\"}")

		uploadFile = request.FILES.get('file',None)				# 获取上传的文件，如果没有文件，则默认为None
		if not uploadFile:
			return HttpResponse("{\"error\" : \"no files for upload\"}")
		
		# 检查资源名是否重名
		finalname = CheckResName(uploadFile.name)
		# 自动生成id
		fileid = GenerateResId(finalname)

		filepath = os.path.join("/root/Resource",finalname).encode("utf-8")
		log_write('info',filepath)
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
		#log_write('info','upload size %s,total size %d',uploadSize,totalsize)
		
		if totalsize != long(uploadSize):
			# 将现有的文件删除
			os.remove(filepath)
			return HttpResponse("{\"error\" : \"upload file failed,not all size\"}")
		
		# 将上传的文件信息保存在数据库中
		SaveResourceToSQL(fileid,finalname,filepath,uploadSize,restype,resdesc)	
		
		return HttpResponse("{\"msg\":\"upload ok\"}")
	else:
		return HttpResponse("{\"error\":\"badmethod\"}")


# 资源删除
def Delete_Resource(request):
	if request.method == 'POST':
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		# 进行认证
		user = CheckAdminToken(oauth)
		if user == None:
			return HttpResponse("{\"error\":\"bad user\"}")
		resid = request.POST.get('resourceid','unkown')
		if resid == 'unkown':
			return HttpResponse("{\"error\":\"bad request\"}")
		strd = '要删除的资源id %s' % resid
		log_write('info',strd)
		bRet = DeleteResourceFromSQL(resid)
		if bRet == False:
			return HttpResponse("{\"error\":\"remove error\"}")
		return HttpResponse("{\"msg\":\"ok\"}")
	else:
		return HttpResponse("{\"error\":\"badmethod\"}")


# 设置用户资源列表
def ResetUserResourceList(request):
	if reqeust.method == 'POST':	
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		# 进行认证
		user = CheckAdminToken(oauth)
		if user == None:
			return HttpResponse("{\"error\":\"bad user\"}")
		res_list = reqeust.POST.get('resourcelist','unkown')
		json_list = json.dumps(res_list)

		SetUserResourceList(json_list)
		return HttpResponse("\"msg\":\"ok\"")
	else:
		return HttpResponse("{\"error\":\"badmethod\"}")

# 获取游戏信息
def GetGameInfo(request):
	if request.method == 'POST':
		oauth = request.META.get('HTTP_AUTHENTICATION','unkown')
		log_write('info','GetGameInfo')
		# 进行认证
		user = CheckUserToken(oauth)
		if user == None:
			return HttpResponse("{\"error\" : \"bad user\"}")
		gameid = request.POST.get("gameid")
		gameinfo = sGameInfoMgr.GetOneGameInfo(gameid)
		if gameinfo != None:
			data_json = gameinfo.ConversionJson()
			return HttpResponse(data_json)
		else:
			return HttpResponse("{\"error\" : \"no game\"}")
	else:
		return HttpResponse("{\"error\":\"badmethod\"}")


