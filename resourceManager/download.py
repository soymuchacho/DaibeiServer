#coding:utf8
from django.http import StreamingHttpResponse
from resourceManager.models import Resource
from login.RsaUtil import *
from base.logger import *

def ResourceDownLoad(resourceId):
	log_write('info','resource download file id : %s',resourceId)
	
	# 从数据库中查找该文件
	dwfile = Resource.objects.filter(resource_id=resourceId)
	if len(dwfile) == 0:
		log_write('info','%s没有这个资源',resourceId)
		return None 
	
	filepath = dwfile.resource_path + '\\' + dwfile.resource_name
	filename = dwfile.resource_name
	log_write('info','找到文件资源：%s ,file id : %s, filepath: %s',filename,resourceId,filepath)
	
	def file_iterator(filepath,chunk_size=512):
		with open(file_name,'rb') as f:
			while True:
				c = f.read(chunk_size)
				if c:
					yield c
				else:
					break
	
	response = StreamingHttpResponse(file_iterator(filepath))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)

	return response 
