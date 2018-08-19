# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from .Sha1 import SHA1 
from base.logger import *
from base.config_xml import *
from django.http import HttpRequest
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.cache import cache
from login.Authentication import CheckUserToken 
from login.Authentication import CheckAdminToken 
from WeiXinInterfaceUrl import *
from WeiXinAccess import *
from WeiChatMaterial import *
import ierror
import urllib
import urllib2
import json
import xml.etree.cElementTree as ET
import time
from base.redis_connect import *
from LeShan import *
from wechat_sdk import WechatBasic
from wechat_sdk import WechatConf
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage, ShortVideoMessage)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


Token = '7539252CA3CB72C1FC8945292164D62E'
EncodingAESKey = 'fQsc2ka2PK5mEJT41zs2iE3dixF9f7Vdr4nENPbJsNG'

SubscriptionToken = '7539252CA3CB72C1FC8945292164D62E'

conf = WechatConf(
	token = '7539252CA3CB72C1FC8945292164D62E',
	appid = WeiXinAppID,
	appsecret = WeiXinSecret,
	encrypt_mode = 'normal',
	encoding_aes_key = 'fQsc2ka2PK5mEJT41zs2iE3dixF9f7Vdr4nENPbJsNG'
)

SubscriptionConf = WechatConf(
	token = SubscriptionToken,
	appid = SubscriptionAppID,
	appsecret = SubscriptionSecret,
	encrypt_mode = 'normal',
)

wechat_instance = WechatBasic(conf=conf)
wechat_subscription_instance = WechatBasic(conf=SubscriptionConf)

LeShanToken = '7123122CA3CB7DBSE8945292164D62E'

# 获取用户信息
def GetWeiXinUserInfo(userOpenID, msgType):
	log_write('info', 'GetWeiXinUserInfo')
	if msgType == "wechat":
		result = wechat_instance.get_user_info(userOpenID)
		return result
	elif msgType == "subscription":
		result = wechat_subscription_instance.get_user_info(userOpenID)
		return result
	return None


def MsgHandle(qrcodeType,userOpenID, touserOpenID, msgType="wechat"):
	out_str = 'MsgHandle userOpenID {0} qrcodeType {1}'.format(userOpenID, qrcodeType)
	log_write('info', out_str)

	result = GetWeiXinUserInfo(userOpenID, msgType)	

	if result == None:
		return None

	out_str = 'user weichat Info {0}'.format(result)
	log_write('info', out_str)

	if result.has_key("nickname"):
		weixinNickName = result['nickname']	
		weixinSex = result['sex']
		openidKey = 'WXOPENID_' + userOpenID
		gametimes = cache.get(openidKey)
		timestr = ''
		timeoldstr = ''
		if gametimes == None:
			timestr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
			gametimes = timestr + ':' + '3'
			out_str = 'user {0} gametimes {1}'.format(openidKey,gametimes)
			log_write('info', out_str)
			cache.set(openidKey,gametimes, timeout=None)
		else:
			timeoldstr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
			strSplit = gametimes.split(':')
			timestr = strSplit[0] 
			if timeoldstr != timestr:
				gametimes = timeoldstr + ':' + '3'
				out_str = 'user {0} gametimes {1}'.format(openidKey,gametimes)
				log_write('info', out_str)
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

def LeShanMsgHandle(NType,weixinname):
	log_write('info', 'LeShanMsgHandle')
	log_write('info', weixinname)
	discounttimes = cache.get(weixinname)
	timestr = ''
	timeoldstr = ''
	if discounttimes == None:
		log_write('info','discounttimes is none')
		timestr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
		log_write('info',timestr)
		discounttimes = timestr + ':' + '0'
		log_write('info',discounttimes)
		cache.set(weixinname,discounttimes, timeout=None)
	else:
		strSplit = discounttimes.split(':')
		i = int(strSplit[1])
		i = i + 1
		discounttimes = timeoldstr + ':' + str(i)

	strSplit = discounttimes.split(":")
	log_write('info', strSplit)
	msg = {
			'msgtype' : NType,
			'username' : weixinname,
			'openid' : weixinname,
			'discounttimes' : strSplit[1]
		}
	msg_json = json.dumps(msg)
	return msg_json


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
@csrf_exempt
def WeiXinCheck(request):
	out_str = 'recv msg from weichat server'
	log_write('info', out_str)
	request.encoding = 'utf8'
	if request.method == 'GET':
		sMsgSignature = request.GET.get('signature')
		sTimestamp = request.GET.get('timestamp')
		sNonce = request.GET.get('nonce')
		sEchoStr = request.GET.get('echostr',None)
		if not wechat_instance.check_signature(signature = sMsgSignature, timestamp=sTimestamp, nonce=sNonce):
			return HttpResponseBadRequest('Verify Failed')

		return HttpResponse(sEchoStr, content_type="text/plain")
	elif request.method == 'POST':
		sMsgSignature = request.GET.get('signature')
		sTimestamp = request.GET.get('timestamp')
		sNonce = request.GET.get('nonce')

		out_str = 'recv msg from weichat server : {0} {1} {2} {3}'.format(sMsgSignature, sTimestamp, sNonce, request.body)
		log_write('info', out_str)

		if not wechat_instance.check_signature(signature = sMsgSignature, timestamp=sTimestamp, nonce=sNonce):
			return HttpResponseBadRequest('Verify Failed')
		
		return_msg = '感谢关注'	
		
		try:
			wechat_instance.parse_data(data=request.body)
		except:
			log_write('info', 'parse xml data error!!')
			return HttpesponseBadRequest('Invalid XML Data')

		channel = g_kRedisMgr.GetRedisConnect().pubsub()
	
		# 获取解析好的微信请求信息
		message = wechat_instance.get_message()

		# 默认消息
		response = wechat_instance.response_text(
				content = return_msg
				)

		if isinstance(message, EventMessage):
			# 收到事件消息
			if message.type == 'subscribe':
				log_write('info', 'guan zhu event')
				# 关注事件
				qrcodeParam = message.key.replace('qrscene_','')
				clientname = qrcodeParam.split("||")[0]
				qrcodeType = qrcodeParam.split("||")[1]

				token = cache.get(clientname)
				out_str = 'parse weichat server msg : qrcodeType {0} clientname {1} token {2}'.format(qrcodeType, clientname, token)
				log_write('info', out_str)	

				msg = MsgHandle(qrcodeType, message.source, message.target)
				channel.subscribe(token)
				g_kRedisMgr.GetRedisConnect().publish(token,msg)
				out_str = 'publish msg token({0}): {1}'.format(token, msg)
				log_write('info', out_str)

				qrInfo = sQrcodeInfoMgr.GetQrcodeInfo(qrcodeType)
				if qrInfo != None:
					jumpNews = sWeChatNewsMgr.GetWeChatNews(qrInfo.GetNewsId())
					response = wechat_instance.response_news(
							[{
								'title' : jumpNews.GetNewsTitle(),
								'description' : jumpNews.GetNewsDesc(),
								'picurl' : jumpNews.GetNewsPicUrl(), 
								'url' : jumpNews.GetNewsUrl(),
							}]
						)	
					out_str = "guanzhu jump news: id {0} title {0}".format(jumpNews.GetNewsId(), jumpNews.GetNewsTitle())
					log_write('info', out_str)
			elif message.type == 'scan':
				#已关注用户扫描二维码事件
				log_write('info', 'scan event')
				log_write('info', message)
				qrcodeParam = message.key
				clientname = qrcodeParam.split("||")[0]
				qrcodeType = qrcodeParam.split("||")[1]
				token = cache.get(clientname)
				out_str = 'parse weichat server msg : qrcodeType {0} clientname {1} token {2} source {3}'.format(qrcodeType, clientname, token,
						message.source)
				log_write('info', out_str)	
			
				if token == None:
					out_str = 'cant find user {0}'.format(clientname)
					log_write('info',out_str)
				else:
					msg = MsgHandle(qrcodeType, message.source, message.target)
					channel.subscribe(token)
					g_kRedisMgr.GetRedisConnect().publish(token,msg)
					out_str = 'publish msg token({0}): {1}'.format(token, msg)
					log_write('info', out_str)
					qrInfo = sQrcodeInfoMgr.GetQrcodeInfo(qrcodeType)
					if qrInfo != None:
						jumpNews = sWeChatNewsMgr.GetWeChatNews(qrInfo.GetNewsId())
						response = wechat_instance.response_news(
							[{
								'title' : jumpNews.GetNewsTitle(),
								'description' : jumpNews.GetNewsDesc(),
								'picurl' : jumpNews.GetNewsPicUrl(), 
								'url' : jumpNews.GetNewsUrl(),
							}]
						)	
					out_str = "scan jump news: id {0} title {0}".format(jumpNews.GetNewsId(), jumpNews.GetNewsTitle())
					log_write('info', out_str)
			elif message.type == 'click':
				# 自定义菜单事件
				buttonInfo = sWeChatButtonMgr.GetWeChatButton(message.key)
				if buttonInfo != None:
					if buttonInfo.GetMsgType() == "msg":
						send_text = ""
						text_split = buttonInfo.GetJumpNews().split("@@")
						for str in text_split:
							send_text += "%s" % str
							send_text += "\n"

						response = wechat_instance.response_text(send_text)
					elif buttonInfo.GetMsgType() == "news":
						jumpNews = sWeChatNewsMgr.GetWeChatNews(buttonInfo.GetJumpNews())
						response = wechat_instance.response_news(
							[{
								'title' : jumpNews.GetNewsTitle(),
								'description' : jumpNews.GetNewsDesc(),
								'picurl' : jumpNews.GetNewsPicUrl(), 
								'url' : jumpNews.GetNewsUrl(),
							}]
						)
						out_str = "click button jump news: id {0} title {0}".format(jumpNews.GetNewsId(), jumpNews.GetNewsTitle())
						log_write('info', out_str)

		return HttpResponse(response, content_type="application/xml")

# 获取带参数的微信二维码
def WeiXinGetQrCode(request):
	request.encoding = 'utf8'
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION', 'unkown') 
		
		log_write('info','-----request weixin QrCode-----');
		
		QrcodeType = request.GET.get("QrcodeType",None)

		# 认证
		user = CheckUserToken(oauth)
		if user == None:
			log_write('info','request weinxin QrCode bad user');
			return HttpResponse("{\"error\" : \"bad user\"}")

		if WeiXinAccessSingleton.WeiXinAccessToken.strip() == '':
			WeiXinAccessSingleton.GetWeiXinAccess()
			
		# 设置参数
		QrcodeInfo = sQrcodeInfoMgr.GetQrcodeInfo(QrcodeType)	
		if QrcodeInfo == None:
			return HttpResponse("{\"error\" : \"bad param\"}")

		scene_str = user.username + '||' + QrcodeInfo.qrcodeParam
		postdata = '{"expire_seconds": 604800, "action_name": "QR_STR_SCENE", "action_info": {"scene": {"scene_str": "' + scene_str + '"}}}'
		
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

# 获取乐山公众号的带参数二维码
def GetLeShanQrcode(request):
	request.encoding = 'utf8'
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION', 'unkown') 
		
		log_write('info','-----request leshan gongzhong hao weixin QrCode-----');
		
		# 认证
		#user = CheckUserToken(oauth)
		#if user == None:
		#	log_write('info','request leshan weinxin QrCode bad user');
		#	return HttpResponse("{\"error\" : \"bad user\"}")

		if LeShanPublishAccessSingleton.LeShanPublishAccessToken.strip() == '':
			LeShanPublishAccessSingleton.GetWeiXinAccess()

		str_out = 'leshanpublish access : {0}'.format(LeShanPublishAccessSingleton.LeShanPublishAccessToken)
		log_write('info',str_out)
		postdata = '{"expire_seconds": 604800, "action_name": "QR_STR_SCENE", "action_info": {"scene": {"scene_str": "test123"}}}'
		reqURL = 'https://' + AccessPoint[0] + GetTemporaryQrCodeUrl + LeShanPublishAccessSingleton.LeShanPublishAccessToken

		str_out = 'reqUrl : {0}'.format(reqURL)
		log_write('info',str_out)
		req = urllib2.Request(url = reqURL, data = postdata)
		res_data = urllib2.urlopen(req)

		res = res_data.read()
		
		result = json.loads(res)
		
		log_write('info','---------------------------1')
		if result.has_key("ticket"):
			ticket = result["ticket"]
		else:
			log_write('info','---------------------------2')
			LeShanPublishAccessSingleton.GetWeiXinAccess()
			reqURL = AccessPoint[0] + GetTemporaryQrCodeUrl + LeShanPublishAccessSingleton.LeShanPublishAccessToken
			req = urllib2.Request(url = reqURL, data = postdata)
			res_data = urllib2.urlopen(req)
		
			log_write('info','---------------------------3')
			res = res_data.read()
			result = json.loads(res)
			if result.has_key("ticket"):
				ticket = result["ticket"]
			else:
				log_write('info','request QrCode : no ticket!');
			log_write('info','---------------------------4')

		log_write('info','---------------------------5')
		if result.has_key("url"):
			qrcodeurl = result["url"]
		
		str = 'request QrCode result : {0} ticket: {1}'.format(res.decode('utf-8'), ticket)
		log_write('info', str)

		ticket_dict = { "ticket" : ticket }
		httpres = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?' + urllib.urlencode(ticket_dict)
		str = 'QrCode http : {0}'.format(httpres.decode('utf-8'))	
		log_write('info',str);
		return HttpResponse(httpres.decode('utf-8'))


# 乐山公众号服务器请求
def LeShanServerNotice(request):
	if request.method == 'GET':
		client = request.GET.get('client', None)
		if client == None:
			return HttpResponse("error")
		weixinid = request.GET.get('weixinid',None)
		if weixinid == None:
			return HttpResponse("error")
		sTimestamp = request.GET.get('timestamps')
		if sTimestamp == None:
			return HttpResponse("error")

		sNType = request.GET.get("NType",None);
		if sNType == None:
			sNType = 'LeShanPublish'

		str_out = 'recv server msg : {0} {1} {2} {3}'.format(client, weixinid, sTimestamp, sNType)
		log_write('info', str_out)

		channel = g_kRedisMgr.GetRedisConnect().pubsub()

		token = cache.get(client)

		str_out = 'parse leshan server msg get client token : {0}'.format(token)
		log_write('info',str_out)

		msg = LeShanMsgHandle(sNType,weixinid)
		
		channel.subscribe(token)
		g_kRedisMgr.GetRedisConnect().publish(token,msg)
		str_out = 'succcess publish msg : {0}'.format(msg)
		log_write('info', str_out)
		return HttpResponse("success")


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


def GongZhongHaoHtml(request):
	if request.method == 'GET':
		return render(request, "gongzhonghao/seal.html");



def CreateMenu(request):
	if request.method == 'POST':
		oauth = request.META.get('HTTP_AUTHENTICATION', 'unkown') 
		wechatType = request.GET.get('wechatType', None) 
		menu = request.body
		# 认证
		admin = CheckAdminToken(oauth)
		if admin == None:
			return HttpResponse("{\"error\" : \"bad user\"}")
		
		if wechatType == None:
			return HttpResponse("{\"error\" : \"bad wechat Type\"}")
		
		menu_dict = eval(menu.decode('utf-8'))
		out_str = 'create menu : {0} type {1}'.format(menu_dict, type(menu_dict))
		log_write('info', out_str)

		if wechatType == "subscription":
			response = wechat_subscription_instance.create_menu(menu_dict)
			json_response = json.dumps(response)
			return HttpResponse(json_response)
		elif wechatType == "wechat":
			response = wechat_instance.create_menu(menu_dict)
			json_response = json.dumps(response)
			return HttpResponse(json_response)
		return HttpResponse("{\"error\" : \"bad Wechat Type\"}")

def GetMenu(request):
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION', 'unkown') 
		wechatType = request.GET.get('wechatType', None) 
		# 认证
		admin = CheckAdminToken(oauth)
		if admin == None:
			return HttpResponse("{\"error\" : \"bad user\"}")
		if wechatType == None:
			return HttpResponse("{\"error\" : \"bad wechat Type\"}")
		
		if wechatType == "subscription":
			response = wechat_subscription_instance.get_menu()
			json_response = json.dumps(response)
			return HttpResponse(json_response)
		elif wechatType == "wechat":
			response = wechat_instance.get_menu()
			json_response = json.dumps(response)
			return HttpResponse(json_response)
		return HttpResponse("{\"error\" : \"bad Wechat Type\"}")
		

def DeleteMenu(request):
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION', 'unkown') 
		wechatType = request.GET.get('wechatType', None) 
	
		# 认证
		admin = CheckAdminToken(oauth)
		if admin == None:
			return HttpResponse("{\"error\" : \"bad user\"}")
		if wechatType == None:
			return HttpResponse("{\"error\" : \"bad Wechat Type\"}")

		if wechatType == "subscription":
			response = wechat_subscription_instance.delete_menu()
			json_response = json.dumps(response)
			return HttpResponse(json_response)
		elif wechatType == "wechat":
			response = wechat_instance.delete_menu()
			json_response = json.dumps(response)
			return HttpResponse(json_response)
		return HttpResponse("{\"error\" : \"bad Wechat Type\"}")


def GetWechatUserList(request):
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION', 'unkown') 
		first_user_id = request.GET.get("first_user_id",None)
		# 认证
		admin = CheckAdminToken(oauth)
		if admin == None:
			return HttpResponse("{\"error\" : \"bad user\"}")
	
		response = ""
		if first_user_id == None:
			response = wechat_instance.get_followers()
		else:
			response = wechat_instance.get_followers(first_user_id)
		
		log_write('info', response)
		log_write('info',type(response))
		json_response = json.dumps(response)
		return HttpResponse(json_response)
		



def SendMessageToUser(request):
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION', 'unkown') 
		message_id = request.GET.get("message_id",None)
		send_user_id = request.GET.get("send_user_id",None)
		# 认证
		admin = CheckAdminToken(oauth)
		if admin == None:
			return HttpResponse("{\"error\" : \"bad user\"}")
	
		if message_id == None:
			return HttpResponse("{\"error\" : \"bad message\"}")
		
		if send_user_id == None:
			return HttpResponse("{\"error\" : \"bad send user\"}")
		
		out_str = "send message to user param : {0} {1} {2}".format(admin, message_id, send_user_id)
		log_write('info', out_str)

		jumpNews = sWeChatNewsMgr.GetWeChatNews(message_id)
		if jumpNews != None:
			response = wechat_instance.send_article_message(send_user_id,
					[{
						'title' : jumpNews.GetNewsTitle(),
						'description' : jumpNews.GetNewsDesc(),
						'picurl' : jumpNews.GetNewsPicUrl(), 
						'url' : jumpNews.GetNewsUrl(),
					}]
					)	
			out_str = "send news to user {0}: id {1} title {2}".format(send_user_id, jumpNews.GetNewsId(), jumpNews.GetNewsTitle())
			log_write('info', out_str)
		else:
			return HttpResponse("{\"error\":\"bad message\"}")

		return HttpResponse("{\"msg\":\"ok\"}")
	


@csrf_exempt
def WeChatSubscription(request):
	request.encoding = 'utf8'
	if request.method == 'GET':
		sMsgSignature = request.GET.get('signature')
		sTimestamp = request.GET.get('timestamp')
		sNonce = request.GET.get('nonce')
		sEchoStr = request.GET.get('echostr',None)
		
		if not wechat_subscription_instance.check_signature(signature = sMsgSignature, timestamp=sTimestamp, nonce=sNonce):
			return HttpResponseBadRequest('Verify Failed')

		return HttpResponse(sEchoStr, content_type="text/plain")
	elif request.method == 'POST':
		sMsgSignature = request.GET.get('signature')
		sTimestamp = request.GET.get('timestamp')
		sNonce = request.GET.get('nonce')

		out_str = 'recv msg from weichat server : {0} {1} {2} {3}'.format(sMsgSignature, sTimestamp, sNonce, request.body)
		log_write('info', out_str)

		if not wechat_subscription_instance.check_signature(signature = sMsgSignature, timestamp=sTimestamp, nonce=sNonce):
			return HttpResponseBadRequest('Verify Failed')
		
		return_msg = '感谢关注'	
		
		try:
			wechat_subscription_instance.parse_data(data=request.body)
		except:
			log_write('info', 'parse xml data error!!')
			return HttpesponseBadRequest('Invalid XML Data')

		# 获取解析好的微信请求信息
		message = wechat_subscription_instance.get_message()

		# 默认消息
		response = wechat_subscription_instance.response_text(
				content = return_msg
				)

		if isinstance(message, EventMessage):
			# 收到事件消息
			if message.type == 'subscribe':
				log_write('info', 'guan zhu event')
				# 关注事件
			elif message.type == 'scan':
				#已关注用户扫描二维码事件
				log_write('info', 'scan event')
				log_write('info', message)
				qrcodeParam = message.key
				clientname = qrcodeParam.split("||")[0]
				qrcodeType = qrcodeParam.split("||")[1]
				token = cache.get(clientname)
				out_str = 'parse weichat server msg : qrcodeType {0} clientname {1} token {2} source {3}'.format(qrcodeType, clientname, token,
						message.source)
				log_write('info', out_str)	
			
				if token == None:
					out_str = 'cant find user {0}'.format(clientname)
					log_write('info',out_str)
				else:
					msg = MsgHandle(qrcodeType, message.source, message.target)
					channel.subscribe(token)
					g_kRedisMgr.GetRedisConnect().publish(token,msg)
					out_str = 'publish msg token({0}): {1}'.format(token, msg)
					log_write('info', out_str)
					qrInfo = sQrcodeInfoMgr.GetQrcodeInfo(qrcodeType)
					if qrInfo != None:
						jumpNews = sWeChatNewsMgr.GetWeChatNews(qrInfo.GetNewsId())
						response = wechat_subscription_instance.response_news(
							[{
								'title' : jumpNews.GetNewsTitle(),
								'description' : jumpNews.GetNewsDesc(),
								'picurl' : jumpNews.GetNewsPicUrl(), 
								'url' : jumpNews.GetNewsUrl(),
							}]
						)	
					out_str = "scan jump news: id {0} title {0}".format(jumpNews.GetNewsId(), jumpNews.GetNewsTitle())
					log_write('info', out_str)
			elif message.type == 'click':
				# 自定义菜单事件
				buttonInfo = sWeChatButtonMgr.GetWeChatButton(message.key)
				if buttonInfo != None:
					if buttonInfo.GetMsgType() == "msg":
						send_text = ""
						text_split = buttonInfo.GetJumpNews().split("@@")
						for str in text_split:
							send_text += "%s" % str
							send_text += "\n"

						response = wechat_subscription_instance.response_text(send_text)
					elif buttonInfo.GetMsgType() == "news":
						jumpNews = sWeChatNewsMgr.GetWeChatNews(buttonInfo.GetJumpNews())
						response = wechat_subscription_instance.response_news(
							[{
								'title' : jumpNews.GetNewsTitle(),
								'description' : jumpNews.GetNewsDesc(),
								'picurl' : jumpNews.GetNewsPicUrl(), 
								'url' : jumpNews.GetNewsUrl(),
							}]
						)
						out_str = "click button jump news: id {0} title {0}".format(jumpNews.GetNewsId(), jumpNews.GetNewsTitle())
						log_write('info', out_str)
		elif isinstance(message, TextMessage):
			# 消息回复
			recv_msg = message.content
			if recv_msg.startswith("@"):
				# 读取机器码，根据机器码找到机器，发送消息给机器	
				param = "?useropenID=%s&machineid=%s&timestamps=%u" % (message.source, recv_msg, message.time)

				response = wechat_subscription_instance.response_text(
						content = '<a href=\"https://lankam.shop/weixinServer/SubscriptionAttention' + param + '\">请点击我</a>'
				)
				return HttpResponse(response)
		return HttpResponse(response, content_type="application/xml")

def SubscriptionAttention(request):
	if request.method == 'GET':
		sMachine = request.GET.get('machineid')
		sUserOpenID = request.GET.get('useropenID')
		sTimestamps = request.GET.get('timestamps')
		if sMachine == None:
			return HttpResponseBadRequest('error number')
		nowTime = time.time()

		if int(nowTime) - int(sTimestamps) > 120:
			return HttpResponseBadRequest('消息已过期')
		
		channel = g_kRedisMgr.GetRedisConnect().pubsub()
		sMachine = sMachine.replace("@","")
		
		token = cache.get(sMachine)			# 根据wechatNumber找到对应的token
		msg = MsgHandle(sMachineID, sUserOpenID, '123', msgType="subscription")

		channel.subscribe(token)
		g_kRedisMgr.GetRedisConnect().publish(token,msg)

		return HttpResponse("感谢关注")	
	else:
		return HttpResponseBadRequest("消息出错")


def GetUploadCardCoverUrl(request): # 上传优惠券封面图

def CreateCards(request): # 创建卡券 
	
def CreateCardLandingPage(request): # 创建货架

def CardConsume(request): # 核销卡券

