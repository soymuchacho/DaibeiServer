# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# 资源
class Resource(models.Model):
	# 资源id
	resource_id = models.CharField(max_length=256)
	# 资源名称
	resource_name = models.CharField(max_length=256)
	# 资源路径
	resource_path = models.CharField(max_length=256)
	# 资源大小
	resource_size = models.IntegerField()
	# 资源类型 
	resource_type = models.CharField(max_length=256)
	# 资源描述
	resource_describe = models.CharField(max_length=1024,null=True)
	# 上传时间
	resource_date = models.CharField(max_length=256,null=True)

	def __unicode__(self):
		return self.resource_id

class ResourceList(models.Model):
	# 所属user
	username = models.CharField(max_length=256)
	# 资源id 
	resource_id = models.CharField(max_length=256)
	
	def __unicode__(self):
		return self.resource_id
	
class UserResourceList(models.Model):
	# 所属user
	username = models.CharField(max_length=256)
	# list version
	list_version = models.CharField(max_length=256)
	
	def __unicode__(self):
		return self.username

