# -*- coding=utf-8 -*-

from base.logger import *
from login.Authentication import CheckUserToken
import json
import os
import sys
import xml.dom.minidom
from xml.dom.minidom import *

class DiscountsInfo():
	def __init__(self, goodsid, gamenum):
		self.goodsid = goodsid
		self.gamenum = gamenum
		self.info_dict = {} 
	
	def GetGoodsID(self):
		return self.goodsid

	def GetPrice(self, goodsid, gameid):
		price = info_dict.get(gameid)
		log_write('info',price)
		return price

	def AddGamePrice(self, gameid, price):
		self.info_dict[gameid] = price
		log_write('info',"AddGamePrice")	

	def ConversionGameDictJson(self):
		json_dict = {}
		json_dict["gamenum"] = self.gamenum
		json_dict["gameinfo"] = self.info_dict
		
		json_data = json.dumps(json_dict)
		str = "Conversion Game DictJson {0}".format(json_data)
		log_write('info',str)
		return json_data

	def ConversionJson(self, gameid):
		price = self.info_dict.get(gameid)
		json_dict = {
			"goodsid" : self.goodsid,
			"gameid" : gameid,
			"price" : price		
		}
		json_data = json.dumps(json_dict)
		str = "ConversionJson {0}".format(json_data)
		log_write('info', str)
		return json_data

class DiscountsMgr():
	def __init__(self):
		self.DiscountsDict = {}

	def AddOneDiscountsInfo(self,disInfo):
		log_write('info','AddOneDiscountsInfo')
		log_write('info',disInfo)
		self.DiscountsDict[disInfo.GetGoodsID()] = disInfo


	def GetOneDiscountsInfo(self,goodsid):
		log_write('info','GetOneGameInfo')
		if self.DiscountsDict.has_key(goodsid):
			return self.DiscountsDict[goodsid]
		else:
			return None

	def Clear(self):
		self.DiscountsDict = {}
	
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

	def Clear(self):
		self.gameDict = {}

sGameInfoMgr = GameInfoMgr()
sDiscountsMgr = DiscountsMgr()

class XmlConfigMgr():

	def __init__(self):
		self.InitGameInfoConfig()	
		self.InitDiscountsInfoConfig()

	def reload(self):
		self.InitGameInfoConfig()	
		self.InitDiscountsInfoConfig()

	def InitGameInfoConfig(self):	
		path = os.path.abspath('.')
		data_path = os.path.join(path,'config/gameinfo.xml')
		log_write('info','init gameinfo xml')
		log_write('info',data_path)
		sGameInfoMgr.Clear()

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
	
	def InitDiscountsInfoConfig(self):
		path = os.path.abspath('.')
		data_path = os.path.join(path,'config/discountsInfo.xml')
		log_write('info','init discontsInfo xml')
		log_write('info',data_path)
		sDiscountsMgr.Clear()
		
		DOMTree = xml.dom.minidom.parse(data_path)
		data = DOMTree.documentElement
		print data
		nodelist = data.getElementsByTagName("discountsInfo")
		print nodelist
		for node in nodelist:
			log_write('info','one node')
			goodsid = node.getAttribute("goodsid") 
			gamenum = node.getAttribute("gamenum") 
			
			disInfo = DiscountsInfo(goodsid, gamenum)
			for num in range(1,int(gamenum)+1):
				attrID = "gameid" + str(num)
				attrPrice = "gameprice" + str(num)

				gameid = node.getAttribute(attrID) 
				gameprice = node.getAttribute(attrPrice)
				
				disInfo.AddGamePrice(gameid, gameprice);

			sDiscountsMgr.AddOneDiscountsInfo(disInfo)

sXmlConfigMgr = XmlConfigMgr()



