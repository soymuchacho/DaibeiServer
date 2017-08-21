#coding=utf-8
import json
from resourceManager.models import *
from base.logger import *

# 保存新上传资源
def SaveResourceToSQL(resid,resname,respath,ressize,restype,resdesc):
	# 从数据库中查看当前资源是否存在
	res = Resource.objects.filter(resource_id=resid)
	if len(res) != 0:
		# 数据库中已经存在.则替换
		res.resource_name = resname
		res.resource_path = respath
		res.resource_size = ressize
		res.resource_type = restype
		res.resource_describe = resdesc
		res.save()
	else:
		# 数据库中不存在
		Resource.objects.create(resource_id=resid,resource_name=resname,resource_path=respath,
				resource_size=long(ressize),resource_type=restype,resource_describe=resdesc)	
		
# 获取用户资源列表版本
def GetResourceListVersion(user):
	if user == None:
		log_write('info','get user resource list version: user is none')
		return None
	log_write('info','get user resource list username %s',user.username)
	
	ret_dict = {} 

	res_info = UserResourceList.objects.filter(username=user.username)
	if len(res_info) == 0:
		log_write('info','get user(%s) resource list version: no list exsits!',user.username)
		return None
	log_write('info','从数据库中获取资源列表成功 %d',len(res_info))	

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
		log_write('info','get user(%s) resource list : no list exsits!',user.username)
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
	log_write('info','get user resource list result : %s',result)
	return result

# 设置用户资源列表
def SetUserResourceList(list_json):
	username = list_json['username']
	#for key,item in enumerate(list_json['resource']):
	#	ResourceList.objects.create(username=username,item[key]['id'])
	return True

# 删除数据库中的资源
def DeleteResourceFromSQL(resid):
	Reource.objects.filter(resource_id = resid).delete()	
	ReourceList.objects.filter(resource_id = resid).delete()	
	return True	
