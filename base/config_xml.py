# -*- coding=utf-8 -*-

from base.logger import *
from login.Authentication import CheckUserToken
import json
import os
import sys
import xml.dom.minidom
from xml.dom.minidom import *

class GameInfo():
	
	def __init__(self,gameid, gamename, price):
		self.gameid = gameid
		self.gamename = gamename
		self.price = price
		str = "gameid {0} gamename {1} price {2}".format(gameid, gamename, price)
		log_write('info',str)
		strjson = self.ConversionJson()
		log_write('info',strjson)

	def GetGameID(self):
		return self.gameid
	
	def GetGameName(self):
		return self.gamename

	def GetPrice(self):
		return self.price

	def ConversionJson(self):
		json_dict = {
					"gameid" : self.gameid,
					"gamename" : self.gamename,
					"price" : self.price
				}
		json_data = json.dumps(json_dict)
		str = "ConversionJson {0}".format(json_data)
		log_write('info',str)
		return json_data

class GameInfoMgr:
	def __init__(self):
		self.gameDict = {}

	def AddOneGameInfo(self,gameInfo):
		log_write('info','AddOneGameInfo')
		log_write('info',gameInfo)
		self.gameDict[gameInfo.GetGameID()] = gameInfo


	def GetOneGameInfo(self,gameid):
		log_write('info','GetOneGameInfo')
		return self.gameDict[gameid]

sGameInfoMgr = GameInfoMgr()

class XmlConfigMgr():

	def __init__(self):
		self.InitGameInfoConfig()	
	
	def InitGameInfoConfig(self):	
		path = os.path.abspath('.')
		data_path = os.path.join(path,'config/gameinfo.xml')
		log_write('info','init gameinfo xml')
		log_write('info',data_path)
		
		DOMTree = xml.dom.minidom.parse(data_path)
		data = DOMTree.documentElement
		print data
		nodelist = data.getElementsByTagName("gameinfo")
		print nodelist
		for node in nodelist:
			log_write('info','one node')
			gameid = node.getAttribute("gameid") 
			gamename = node.getAttribute("gamename") 
			gameprice = node.getAttribute("price") 
			gameInfo = GameInfo(gameid, gamename, gameprice)
			sGameInfoMgr.AddOneGameInfo(gameInfo)

sXmlConfigMgr = XmlConfigMgr()



