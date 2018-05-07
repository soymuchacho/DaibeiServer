#coding=utf-8
import json
import time
import hashlib
import redis
from base.logger import *
from base.defines import *
from login.models import User_Info


class Machine:
	def __init__(self, username, token, location, manager, useTime, isOnline):
		self.username = username
		self.token = token
		self.location = location
		self.manager = manager
		self.useTime = useTime
		self.isOnline = isOnline
	
	def SetOnline(self):
		str = "set machine online {0} {1}".format(self.username, self.token)
		log_write('info', str)
		self.isOnline = 1

	def IsOnline(self):
		return self.isOnline

	def GetMachineToken(self):
		return self.token

	def SendMsgToMachine(self, msg):
		if self.isOnline == 1:
			log_write('info', "is online publish operator")
			try:
				r = redis.StrictRedis(host="127.0.0.1", port=6379, db = 0)
				log_write('info', "publish operator")
				log_write('info', self.token)
				channel = r.publish(self.token, msg)
				return True
			except:
				return False
		else:
			return False

class MachineMgr:
	def __init__(self):
		self.userDic = {} 
		self.tokenDic = {}

	def MachineLogin(self, username, token, location, manager, useTime):
		if self.userDic.has_key(username) and self.tokenDic.has_key(token):
			self.userDic[username].SetOnline()
			self.tokenDic[token].SetOnline()
		else:
			str = "machine login {0} {1} {2} {3} {4} ".format(username, token, location, manager, useTime)
			log_write('info', str)
			kMachine = Machine(username, token, location, manager, useTime, 0)
			self.userDic[username] = kMachine
			self.tokenDic[token] = kMachine
	
	def MachineOffLine(self, username, token):
		str = "machine offline {0} {1}".format(username, token)
		log_write('info', str)
		if self.userDic.has_key(username):
			self.userDic.pop(username)
		if self.tokenDic.has_key(token):
			self.tokenDic.pop(token)

	def SetMachineOnLine(self, username, token):
		if self.userDic.has_key(username) and self.tokenDic.has_key(token):
			self.userDic[username].SetOnline()
			self.tokenDic[token].SetOnline()
			return True
		else:
			return False

	def IsMachineOnline(self, username):
		if self.userDic.has_key(username):
			return self.userDic[username].IsOnline()
		else:
			return 0

	def ShutDownMachine(self, username):
		if self.userDic.has_key(username):
			if self.userDic[username].IsOnline() == 1:
				OpStr = '{\"token\":\"' + self.userDic[username].GetMachineToken() + '\", \"operate\":\"shutdown\"}'
				return self.userDic[username].SendMsgToMachine(OpStr)				
			else:
				return False
		else:
			return False

g_kMachineMgr = MachineMgr();


