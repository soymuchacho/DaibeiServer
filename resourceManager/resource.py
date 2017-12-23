#coding=utf-8
import json
import time
import os
import hashlib
from resourceManager.models import *
from base.logger import *


RESOURCE_PAGE_DEFAULT_NUMBER = 10


def GetAllResourcePageCount():
	total = Resource.objects.all().count()
	page = total / RESOURCE_PAGE_DEFAULT_NUMBER
	
	end = total % RESOURCE_PAGE_DEFAULT_NUMBER
	if end != 0:
		page = page + 1
	return page


# 获取全部资源
def GetAllResourceFromSQL(page):
	if page < 1:
		return None
	begin = (page - 1) * RESOURCE_PAGE_DEFAULT_NUMBER
	end = page * RESOURCE_PAGE_DEFAULT_NUMBER
	reslist = Resource.objects.all()[begin:end]
	if len(reslist) == 0:
		return None
	return reslist

# 检查资源是否重名，若重名则在名字后加后缀
def CheckResName(resname):
	index = 0
	(shotname,ext) = os.path.splitext(resname)
	tempname = shotname 
	while True:
		index = index + 1
		finalname = tempname + ext
		res = Resource.objects.filter(resource_name=finalname)
		if len(res) == 0:
			return finalname 
		else:
			tempname = shotname + '(' + str(index) + ')';

# 根据文件名自动生成资源id
def GenerateResId(resname):
	m2 = hashlib.md5()
	m2.update(resname.encode('utf-8'))
	return m2.hexdigest()

# 保存新上传资源
def SaveResourceToSQL(resid,resname,respath,ressize,restype,resdesc):
	log_write('info',resname)
	# 从数据库中查看当前资源是否存在
	res = Resource.objects.filter(resource_id=resid)
	now_time = time.strftime("%Y-%02m-%02d %02H:%02M:%02S",time.localtime(time.time()))
	if len(res) != 0:
		# 数据库中已经存在.则替换
		res[0].resource_name = resname
		res[0].resource_path = respath
		res[0].resource_size = ressize
		res[0].resource_type = restype
		res[0].resource_describe = resdesc
		res[0].resource_date = now_time
		res[0].save()
	else:
		# 数据库中不存在
		Resource.objects.create(resource_id=resid,resource_name=resname,resource_path=respath,
				resource_size=long(ressize),resource_type=restype,resource_describe=resdesc,resource_date=now_time)	
		
# 获取用户资源列表版本
def GetResourceListVersion(user):
	if user == None:
		log_write('info','get user resource list version: user is none')
		return None
	#log_write('info','get user resource list username %s',user.username)
	
	ret_dict = {} 

	res_info = UserResourceList.objects.filter(username=user.username)
	if len(res_info) == 0:
		#log_write('info','get user(%s) resource list version: no list exsits!',user.username)
		return None
	#log_write('info','从数据库中获取资源列表成功 %d',len(res_info))	

	# 获取list版本
	list_ver = res_info[0].list_version

	ret_dict['version'] = list_ver
	
	result = json.dumps(ret_dict)
	return result


# 获取用户资源列表
def GetResourceList(user):
	if user == None:
		log_write('info','get user resource list : user is none')
		return None

	res_info = UserResourceList.objects.filter(username=user.username)
	if len(res_info) == 0:
		#log_write('info','get user(%s) resource list : no list exsits!',user.username)
		return None

	ret_dict = {}

	# 获取list版本
	list_ver = res_info[0].list_version
	ret_dict['version'] = list_ver
#	log_write('info','get user(%s) resource list : version %s',user.username,list_ver)

	# 获取list内容
	res_list = ResourceList.objects.filter(username=user.username)
	if len(res_list) == 0:
		result = json.dumps(ret_dict)
		return result
	
	ret_dict['resource'] = [] 
	for resource in res_list:
		node_dict = {}	
		node_dict['id'] = resource.resource_id
		# 根据id查找资源信息
		res = Resource.objects.filter(resource_id=resource.resource_id)
		if len(res) != 0:
			node_dict['name'] = res[0].resource_name
			node_dict['type'] = res[0].resource_type
			node_dict['size'] = res[0].resource_size
			node_dict['describe'] = res[0].resource_describe
		ret_dict['resource'].append(node_dict)

	result = json.dumps(ret_dict)
	#log_write('info','get user resource list result : %s',result)
	return result

# 设置用户资源列表
def SetUserResourceList(list_json):
	username = list_json['username']
	#for key,item in enumerate(list_json['resource']):
	#	ResourceList.objects.create(username=username,item[key]['id'])
	return True

# 删除数据库中的资源
def DeleteResourceFromSQL(resid):
	res = Resource.objects.filter(resource_id=resid)
	if len(res) == 0:
		return False
	filepath = res[0].resource_path
	log_write('info',filepath)
	try:
		os.remove(filepath.encode('utf-8'))
	except:
		log_write('info','文件删除错误')
		return False
	res.delete()
	ResourceList.objects.filter(resource_id = resid).delete()	
	log_write('info','资源已删除')
	return True	
