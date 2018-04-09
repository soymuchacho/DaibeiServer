# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .Sha1 import SHA1 
from base.logger import *
from django.http import HttpRequest
from django.http import HttpResponse
from django.core.cache import cache
from login.Authentication import CheckUserToken 
from WeiXinInterfaceUrl import *
from WeiXinAccess import *
import ierror
import urllib
import urllib2
import json
import xml.etree.cElementTree as ET
import redis
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

Token = '7539252CA3CB72C1FC8945292164D62E'
EncodingAESKey = 'fQsc2ka2PK5mEJT41zs2iE3dixF9f7Vdr4nENPbJsNG'

# 获取用户信息
def GetWeiXinUserInfo(userOpenID):
	log_write('info', 'GetWeiXinUserInfo')
	i = 0
	if WeiXinAccessSingleton.WeiXinAccessToken == '':
		WeiXinAccessSingleton.GetWeiXinAccess()
	while True:
		reqUrl = 'https://' + AccessPoint[0] + GetWeiXinUserInfoUrl + 'access_token=' + WeiXinAccessSingleton.WeiXinAccessToken + '&openid=' + userOpenID + '&lang=zh_CN'
		log_write('info', reqUrl)
		req = urllib2.Request(url = reqUrl)
		res_data = urllib2.urlopen(req)

		res = res_data.read()
		result = json.loads(res)
		log_write('info', result)
		if result.has_key('errcode'):
			WeiXinAccessSingleton.GetWeiXinAccess()
			i = 1
		else:
			break
		if i == 1:
			return result
	return result

def MsgHandle(userOpenID):
	log_write('info', 'MsgHandle')
	log_write('info', userOpenID)
	result = GetWeiXinUserInfo(userOpenID)	
	log_write('info', 'GetWeiXinUserInfo')
	log_write('info', result)
	if result.has_key("nickname"):
		log_write('info', 'result has key nickname')
		weixinNickName = result['nickname']	
		weixinSex = result['sex']
		log_write('info',weixinNickName)
		log_write('info',weixinSex)
		openidKey = 'WXOPENID_' + userOpenID
		log_write('info',openidKey)
		gametimes = cache.get(openidKey)
		timestr = ''
		timeoldstr = ''
		if gametimes == None:
			log_write('info','gametimes is none')
			timestr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
			log_write('info',timestr)
			gametimes = timestr + ':' + '3'
			log_write('info',gametimes)
			cache.set(openidKey,gametimes, timeout=None)
		else:
			timeoldstr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
			strSplit = gametimes.split(':')
			timestr = strSplit[0] 
			if timeoldstr != timestr:
				gametimes = timeoldstr + ':' + '3'
				cache.set(openidKey,gametimes, timeout=None)
		
		strSplit = gametimes.split(":")
		log_write('info', strSplit)
		msg = {
				'msgtype' : 'GameTimes',
				'username' : weixinNickName,
				'openid' : openidKey,
				'gametimes' : strSplit[1]
		}
		msg_json = json.dumps(msg)
		return msg_json
	else:
		log_write('info', 'MsgHandle None')
		return None
# 微信验证
def WeiXinCheckTest(request):
		log_write('info', request.body)
		log_write('info', 'parse begin')
		# 进行数据解析
	
		xml_tree = ET.fromstring(request.body)
		touser_name    = xml_tree.find("ToUserName")
		fromOpenID    = xml_tree.find("FromUserName")
		event = xml_tree.find("Event")
		eventKey = xml_tree.find("EventKey")
		log_write('info', eventKey)
		log_write('info', 'parse End')
		log_write('info', 'parse End')
		if event.text == 'subcribe':
			log_write('info', eventKey.text)
			msg = MsgHandle(fromOpenID.text)
	#		eventKey.replace('qrscene_','')
			log_write('info', eventKey.text)
		elif event.text == 'SCAN':
			log_write('info','scan')
			log_write('info', eventKey.text)
			token = cache.get(eventKey.text)
			if token == None:
				log_write('info','no user')
			else:
				log_write('info',token)
				log_write('info',fromOpenID.text)
				msg = MsgHandle(fromOpenID.text)
				log_write('info',msg)
		log_write('info', 'success')
		return_msg = '<xml> <ToUserName>< ![CDATA['+fromOpenID.text+'] ]></ToUserName> <FromUserName>< ![CDATA[' + touser_name.text + '] ]></FromUserName> <CreateTime>' + str(int(time.time())) + '</CreateTime> <MsgType>< ![CDATA[text] ]></MsgType> <Content>< ![CDATA[感谢您对兰凯互动的关注] ]></Content> </xml>'
		log_write('info',return_msg)
		returnxml = ET.tostring(return_msg.encode('utf-8'))
		log_write('info',returnxml)
		return HttpResponse('success');


# 微信验证
def WeiXinCheck(request):
	log_write('info', 'wei xin check')
	request.encoding = 'utf8'
	log_write('info', request)
	if request.method == 'POST':
		sMsgSignature = request.GET.get('signature')
		sTimestamp = request.GET.get('timestamp')
		sNonce = request.GET.get('nonce')

		log_write('info', sMsgSignature)
		log_write('info', sTimestamp)
		log_write('info', sNonce)
		log_write('info', request.body)
		ret,signature = SHA1().getSHA1(Token, sTimestamp, sNonce, '')
		if ret != 0:
			log_write('info', ret)
			log_write('info', signature)
			return ret,None
		else:
			if not signature == sMsgSignature:
				return ierror.WXBizMsgCrypt_ValidateSignature_Error, None
		return_msg = 'success'	
		log_write('info', 'parse begin')
		# 进行数据解析
	
		xml_tree = ET.fromstring(request.body)
		touser_name    = xml_tree.find("ToUserName")
		fromOpenID    = xml_tree.find("FromUserName")
		event = xml_tree.find("Event")
		eventKey = xml_tree.find("EventKey")
		log_write('info', eventKey)
		log_write('info', 'parse End')
		log_write('info', 'parse End')
		r = redis.StrictRedis(host="127.0.0.1",port=6379, db = 0); 
		channel = r.pubsub()
		
		if event.text == 'subscribe':
			log_write('info',' event subcribe')
			log_write('info', eventKey.text)
			clientname = eventKey.text.replace('qrscene_','')
			token = cache.get(clientname)
			log_write('info', token)
			msg = MsgHandle(fromOpenID.text)
			log_write('info',msg)
			log_write('info','channel pubsub');	
			channel.subscribe(token)
			log_write('info','redis pubsub channel...');	
			r.publish(token,msg)
		elif event.text == 'SCAN':
			log_write('info','scan')
			log_write('info', eventKey.text)
			token = cache.get(eventKey.text)
			if token == None:
				log_write('info','no user')
			else:
				log_write('info',token)
				log_write('info',fromOpenID.text)
				msg = MsgHandle(fromOpenID.text)
				log_write('info',msg)
				log_write('info','channel pubsub');	
				channel.subscribe(token)
				log_write('info','redis pubsub channel...');	
				r.publish(token,msg)
		else:
			log_write('info',event.text)
		log_write('info', 'success')
		return HttpResponse(return_msg)

# 获取带参数的微信二维码
def WeiXinGetQrCode(request):
	request.encoding = 'utf8'
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION', 'unkown') 
		
		log_write('info','-----request weixin QrCode-----');
		
		# 认证
		user = CheckUserToken(oauth)
		if user == None:
			log_write('info','request weinxin QrCode bad user');
			return HttpResponse("{\"error\" : \"bad user\"}")

		# 设置参数

		if WeiXinAccessSingleton.WeiXinAccessToken.strip() == '':
			WeiXinAccessSingleton.GetWeiXinAccess()

		postdata = '{"expire_seconds": 604800, "action_name": "QR_STR_SCENE", "action_info": {"scene": {"scene_str": "' + user.username + '"}}}'
		reqURL = 'https://' + AccessPoint[0] + GetTemporaryQrCodeUrl + WeiXinAccessSingleton.WeiXinAccessToken

		req = urllib2.Request(url = reqURL, data = postdata)
		res_data = urllib2.urlopen(req)

		res = res_data.read()
		result = json.loads(res)
			
		if result.has_key("ticket"):
			ticket = result["ticket"]
		else:
			WeiXinAccessSingleton.GetWeiXinAccess()
			reqURL = AccessPoint[0] + GetTemporaryQrCodeUrl + WeiXinAccessSingleton.WeiXinAccessToken
			req = urllib2.Request(url = reqURL, data = postdata)
			res_data = urllib2.urlopen(req)
		
			res = res_data.read()
			result = json.loads(res)
			if result.has_key("ticket"):
				ticket = result["ticket"]
			else:
				log_write('info','request QrCode : no ticket!');

		if result.has_key("url"):
			qrcodeurl = result["url"]
		
		str = 'request QrCode result : {0} ticket: {1}'.format(res.decode('utf-8'), ticket)
		log_write('info', str)

		ticket_dict = { "ticket" : ticket }
		httpres = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?' + urllib.urlencode(ticket_dict)
		str = 'QrCode http : {0}'.format(httpres.decode('utf-8'))	
		log_write('info',str);
		return HttpResponse(httpres.decode('utf-8'))


# 微信用户玩过一次游戏
def WeiXinUserPlayedGame(request):
	request.encoding = 'utf8'
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION', 'unkown') 
		weixinaccount = request.GET.get('weixinaccount')	
		log_write('info', 'WeiXinUserPlayedGame')
		log_write('info', weixinaccount)
		# 认证
		user = CheckUserToken(oauth)
		if user == None:
			return HttpResponse("{\"error\" : \"bad user\"}")
		gametimes = cache.get(weixinaccount)
		if gametimes == None:
			return HttpResponse("{\"msg\" : \"err\"}")
		
		timestr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		log_write('info',timestr)
		strSplit = gametimes.split(":")
		times = int(strSplit[1]) - 1
		if times < 0:
			times = 0
		strTimes = str(times)
		uservalue = timestr + ':' + strTimes
		log_write('info',uservalue)
		cache.set(weixinaccount, uservalue, timeout=None)
		return HttpResponse("{\"msg\" : \"ok\"}")
	else:	
		return HttpResponse("{\"msg\" : \"BAD Request\"}")
