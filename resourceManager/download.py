#coding:utf-8
import json
import os
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from resourceManager.models import Resource
from login.RsaUtil import *
from base.logger import *
from wsgiref.util import FileWrapper

def ResourceDownLoad(resourceId):
	log_write('info','resource download file id : %s',resourceId)
	
	# 从数据库中查找该文件
	dwfile = Resource.objects.filter(resource_id=resourceId)
	if len(dwfile) == 0:
		log_write('info','%s没有这个资源',resourceId)
		return None 
	
	filepath = dwfile[0].resource_path.encode('utf8')
	filename = dwfile[0].resource_name
	#log_write('info','找到文件资源：%s ,file id : %s, filepath: %s',filename,resourceId,filepath)

	wrapper = FileWrapper(file(filepath))
	#def file_iterator(filepath,chunk_size=512):
	#	try:
	#		with open(filepath,'rb') as f:
	#			while True:
	#				c = f.read(chunk_size)
	#				if c:
	#					yield c
	#				else:
	#					break
	#	except:
	#		raise Http404
	
	#response = StreamingHttpResponse(file_iterator(filepath))
	response = HttpResponse(wrapper,content_type='text/plain')
	response['Content-Length'] = os.path.getsize(filepath)
	response['Content-Disposition']='attachment;filename={0}'.format(filename.encode('utf8'))	
	dic_ret = {}
	dic_ret['id'] = dwfile[0].resource_id
	dic_ret['name'] = dwfile[0].resource_name
	dic_ret['type'] = dwfile[0].resource_type
	json_str = json.dumps(dic_ret)
	
	#response['content'] = json_str

	return response 
