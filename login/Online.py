#coding=utf-8
import json
import time
import hashlib
from base.redis_connect import *
from base.logger import *
from base.defines import *
from login.models import User_Info

class Machine:
	def __init__(self, username, token, location, manager, useTime, isOnline, wechatType, wechatNumber):
		self.username = username
		self.token = token
		self.location = location
		self.manager = manager
		self.useTime = useTime
		self.wechatType = wechatType
		self.wechatNumber = wechatNumber
		self.isOnline = isOnline
		self.webSocketConnect = False
		self.pubsub = None

	def SetOnline(self):
		str = "set machine online {0} {1}".format(self.username, self.token)
		log_write('info', str)
		self.isOnline = 1

	def ConnectWebSocket(self):
		self.pubsub = g_kRedisMgr.GetReidsWebConnection().pubsub()

	def SetWebSocketConnect(self, bIsConnect):
		self.webSocketConnect = bIsConnect

	def IsWebSocketConnect(self):
		return self.webSocketConnect

	def CloseWebSocket(self):
		self.pubsub.quit()
		log_write('info', "websocket old close")

	def GetWebPubsub(self):
		return self.pubsub

	def IsOnline(self):
		return self.isOnline

	def GetMachineToken(self):
		return self.token

	def SendMsgToMachine(self, msg):
		if self.isOnline == 1:
			log_write('info', "is online publish operator")
			try:
				log_write('info', "publish operator")
				log_write('info', self.token)
				channel = g_kRedisMgr.GetRedisWebConnect().publish(self.token, msg)
				return True
			except:
				return False
		else:
			return False

class MachineMgr:
	def __init__(self):
		self.userDic = {} 
		self.tokenDic = {}

	def MachineLogin(self, username, token, location, manager, useTime, wechatType, wechatNumber):
		if self.userDic.has_key(username) and self.tokenDic.has_key(token):
			self.userDic[username].SetOnline()
			self.tokenDic[token].SetOnline()
		else:
			str = "machine login {0} {1} {2} {3} {4} {5} {6}".format(username, token, location, manager, useTime, wechatType, wechatNumber)
			log_write('info', str)
			kMachine = Machine(username, token, location, manager, useTime, 0, wechatType, wechatNumber)
			self.userDic[username] = kMachine
			self.tokenDic[token] = kMachine

	def ConnectWebSocket(self, username, token):
		if self.userDic.has_key(username) and self.tokenDic.has_key(token):
			self.userDic[username].ConnectWebSocket()
			self.tokenDic[token].ConnectWebSocket()
			
	def CloseWebSocket(self, username, token):
		if self.userDic.has_key(username) and self.tokenDic.has_key(token):
			self.userDic[username].CloseWebSocket()
			self.tokenDic[token].CloseWebSocket()

	def GetWebPubsub(self, username, token):
		if self.userDic.has_key(username) and self.tokenDic.has_key(token):
			return self.userDic[username].GetWebPubsub()

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

	def IsMachineOnLine(self, username, token):
		if self.userDic.has_key(username) and self.tokenDic.has_key(token):
			if self.userDic[username].IsOnline() == 1:
				return True
			else:
				return False
		else:
			return False

	def SetWebSocketConnect(self, username, token, bIsConnect):
		if self.userDic.has_key(username) and self.tokenDic.has_key(token):
			self.userDic[username].SetWebSocketConnect(bIsConnect)
			self.tokenDic[token].SetWebSocketConnect(bIsConnect)
			return True
		else:
			return False

	def IsWebSocketConnect(self, username, token):
		if self.userDic.has_key(username) and self.tokenDic.has_key(token):
			return self.userDic[username].IsWebSocketConnect()
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


