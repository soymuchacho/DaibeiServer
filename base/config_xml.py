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

class QrcodeInfo():
	def __init__(self, qrcodeType, qrcodeParam, newsId):
		self.qrcodeType = qrcodeType				# 二维码类型
		self.qrcodeParam = qrcodeParam				# 二维码参数
		self.newsId = newsId						# 消息id

	def GetNewsId(self):
		return self.newsId

class QrcodeConfigMgr():
	def __init__(self):
		self.qrcodeInfos = {}
	
	def AddOneQrcode(self, qrcodeType, qrcodeParam, newsId):
		#str = 'add one qrcode info : {0} {1} {2} {3} {4} {5} '.format(qrcodeType, qrcodeParam, title, description, picurl, url)
		#log_write('info', str)
		info = QrcodeInfo(qrcodeType, qrcodeParam, newsId)
		self.qrcodeInfos[qrcodeType] = info

	def GetQrcodeInfo(self, qrcodeType):
		if self.qrcodeInfos.has_key(qrcodeType):
			return self.qrcodeInfos[qrcodeType]
		return None
	
	def Clear(self):
		self.qrcodeInfos = {}

sQrcodeInfoMgr = QrcodeConfigMgr()

class WeChatNews():
	def __init__(self, newsId, newsTitle, newsDesc, newsPicUrl, newsUrl):
		self.newsId = newsId
		self.newsTitle = newsTitle
		self.newsDesc = newsDesc
		self.newsPicUrl = newsPicUrl
		self.newsUrl = newsUrl

	def GetNewsId(self):
		return self.newsId

	def GetNewsTitle(self):
		return self.newsTitle

	def GetNewsDesc(self):
		return self.newsDesc

	def GetNewsPicUrl(self):
		return self.newsPicUrl

	def GetNewsUrl(self):
		return self.newsUrl

class WeChatNewsMgr():
	def __init__(self):
		self.WeChatNewsMap = {}

	def AddWeChatNews(self, newsId, newsTitle, newsDesc, newsPicUrl, newsUrl):
		news = WeChatNews(newsId, newsTitle, newsDesc, newsPicUrl, newsUrl)
		self.WeChatNewsMap[newsId] = news

	def GetWeChatNews(self, newsId):
		if self.WeChatNewsMap.has_key(newsId):
			return self.WeChatNewsMap[newsId]
		else:
			return None
	
	def Clear(self):
		self.WeChatNewsMap = {}

sWeChatNewsMgr = WeChatNewsMgr()

class WeChatButton():
	def __init__(self, ButtonKey, MsgType, JumpNews):
		self.ButtonKey = ButtonKey
		self.MsgType = MsgType
		self.JumpNews = JumpNews

	def GetButtonKey(self):
		return self.ButtonKey

	def GetMsgType(self):
		return self.MsgType

	def GetJumpNews(self):
		return self.JumpNews

class WeChatButtonMgr():
	def __init__(self):
		self.WeChatButtonMap = {}

	def AddWeChatButton(self, ButtonKey, MsgType, JumpNews):
		newButton = WeChatButton(ButtonKey, MsgType, JumpNews)
		self.WeChatButtonMap[ButtonKey] = newButton

	def GetWeChatButton(self, ButtonKey):
		if self.WeChatButtonMap.has_key(ButtonKey):
			return self.WeChatButtonMap[ButtonKey]
		else:
			return None

	def Clear(self):
		self.WeChatButtonMap = {}

sWeChatButtonMgr = WeChatButtonMgr()

class Machine():
	def __init__(self, machineid, wechatNumber):
		self.machineID = machineid
		self.wechatNumber = wechatNumber

	def GetMachineID(self):
		return self.machineID

	def GetWechatNumber(self):
		return self.wechatNumber

class MachineMgr():
	def __init__(self):
		machines = {}

	def AddMachine(self, machineID, wechatNumber):
		newMachine = Machine(machineID, wechatNumber)
		self.machines[wechatNumber] = newMachine

	def GetMachineIDByWechatNumber(self, wechatNumber):
		if self.machines.has_key(wechatNumber):
			return self.machines[wechatNumber].GetMachineID()
		return None

	def Clear(self):
		self.machines = {}

sMachineMgr = MachineMgr()

class XmlConfigMgr():

	def __init__(self):
		self.InitGameInfoConfig()	
		self.InitDiscountsInfoConfig()
		self.InitQrcodeInfoConfig()
		self.InitWeChatButtonConfig()
		self.InitWeChatNewsConfig()
		self.InitMachineInfo()

	def reload(self):
		self.InitGameInfoConfig()	
		self.InitDiscountsInfoConfig()
		self.InitQrcodeInfoConfig()
		self.InitWeChatButtonConfig()
		self.InitWeChatNewsConfig()
		self.InitMachineInfo()

	def InitGameInfoConfig(self):	
		path = os.path.abspath('.')
		data_path = os.path.join(path,'config/gameinfo.xml')
		log_write('info','init gameinfo xml')
		log_write('info',data_path)
		sGameInfoMgr.Clear()

		DOMTree = xml.dom.minidom.parse(data_path)
		data = DOMTree.documentElement
		nodelist = data.getElementsByTagName("gameinfo")
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
		nodelist = data.getElementsByTagName("discountsInfo")
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
	
	def InitQrcodeInfoConfig(self):
		path = os.path.abspath('.')
		data_path = os.path.join(path, 'config/qrcodeInfo.xml')

		out_str = 'init qrcodeInfo xml : {0}'.format(data_path)
		log_write('info', out_str)

		sQrcodeInfoMgr.Clear()
		DOMTree = xml.dom.minidom.parse(data_path)
		data = DOMTree.documentElement
		nodelist = data.getElementsByTagName("qrcodeInfo")
		for node in nodelist:
			qrcodeType = node.getAttribute("qrtype")
			qrcodeParam = node.getAttribute("qrparam")
			newsId = node.getAttribute("NewsId")
			
			#out_str = 'read from qrcodeconfig xml : {0} {1} {2}'.format(qrcodeType, qrcodeParam, resTitle)
			#log_write('info', out_str)

			sQrcodeInfoMgr.AddOneQrcode(qrcodeType, qrcodeParam, newsId)

	def InitWeChatNewsConfig(self):
		path = os.path.abspath('.')
		data_path = os.path.join(path, 'config/WeChatNews.xml')

		out_str = 'init WeChatNews xml : {0}'.format(data_path)
		log_write('info', out_str)

		sWeChatNewsMgr.Clear()
		DOMTree = xml.dom.minidom.parse(data_path)
		data = DOMTree.documentElement
		nodelist = data.getElementsByTagName("News")
		for node in nodelist:
			newsId = node.getAttribute("id")
			newsTitle = node.getAttribute("title")
			newsDesc = node.getAttribute("desc")
			newsPicUrl = node.getAttribute("picurl")
			newsUrl = node.getAttribute("url")
			
			sWeChatNewsMgr.AddWeChatNews(newsId, newsTitle, newsDesc, newsPicUrl, newsUrl)


	def InitWeChatButtonConfig(self):
		path = os.path.abspath('.')
		data_path = os.path.join(path, 'config/WeChatButton.xml')

		out_str = 'init WeChatButton xml : {0}'.format(data_path)
		log_write('info', out_str)

		sWeChatButtonMgr.Clear()
		DOMTree = xml.dom.minidom.parse(data_path)
		data = DOMTree.documentElement
		nodelist = data.getElementsByTagName("button")
		for node in nodelist:
			ButtonKey = node.getAttribute("key")
			MsgType = node.getAttribute("newsType")
			ButtonJump = node.getAttribute("jumpNews")
			
			sWeChatButtonMgr.AddWeChatButton(ButtonKey, MsgType, ButtonJump)

	def InitMachineInfo(self):
		path = os.path.abspath('.')
		data_path = os.path.join(path, 'config/Machine.xml')

		out_str = 'init Machine xml : {0}'.format(data_path)
		log_write('info', out_str)

		sMachineMgr.Clear()
		DOMTree = xml.dom.minidom.parse(data_path)
		data = DOMTree.documentElement
		nodelist = data.getElementsByTagName("Machine")
		for node in nodelist:
			machineID = node.getAttribute("machineid")
			wechatNumber = node.getAttribute("wechatnumber")
			
			sMachineMgr.AddMachine(machineID, wechatNumber)

sXmlConfigMgr = XmlConfigMgr()



