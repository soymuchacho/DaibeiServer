#coding=utf-8
import json
import time
import hashlib
from login.models import User_Info
from login.models import Admin_Info

PAGE_DEFAULT_NUMBER = 10

def GetAllUserListPageCount():
	total = GetAllUserListNum();
	page = total / PAGE_DEFAULT_NUMBER
	
	end = total % PAGE_DEFAULT_NUMBER
	if end != 0:
		page = page + 1
	return page

def GetAllUserListNum():
	total = User_Info.objects.all().count()
	return total

def GetAllUserListFromSQL(page):
	if page < 1:
		return None
	begin = (page-1) * PAGE_DEFAULT_NUMBER
	end = page * PAGE_DEFAULT_NUMBER
	userlist = User_Info.objects.all()[begin:end]
	if len(userlist) == 0:
		return None
	return userlist

