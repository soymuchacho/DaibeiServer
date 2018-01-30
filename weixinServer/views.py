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
from ParseXml import *
import ierror
import urllib
import urllib2
import json

Token = '7539252CA3CB72C1FC8945292164D62E'
EncodingAESKey = 'fQsc2ka2PK5mEJT41zs2iE3dixF9f7Vdr4nENPbJsNG'

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

		log_write('info', 'success')
		return HttpResponse('success');

# 获取带参数的微信二维码
def WeiXinGetQrCode(request):
	request.encoding = 'utf8'
	if request.method == 'GET':
		oauth = request.META.get('HTTP_AUTHENTICATION', 'unkown') 
		
		# 认证
		user = CheckUserToken(oauth)
		if user == None:
			return HttpResponse("{'error' : 'bad user'}")

		# 设置参数

		if WeiXinAccessSingleton.WeiXinAccessToken.strip() == '':
			WeiXinAccessSingleton.GetWeiXinAccess()

		postdata = '{"expire_seconds": 604800, "action_name": "QR_STR_SCENE", "action_info": {"scene": {"scene_str": "' + user.username + '"}}}'
		log_write('info', WeiXinAccessSingleton.WeiXinAccessToken)
		reqURL = 'https://' + AccessPoint[0] + GetTemporaryQrCodeUrl + WeiXinAccessSingleton.WeiXinAccessToken
		log_write('info', reqURL)
		log_write('info', postdata)
	
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
		
			res = res_data.read()
			result = json.loads(res)
			if result.has_key("ticket"):
				ticket = result["ticket"]
			
		if result.has_key("url"):
			qrcodeurl = result["url"]
		
		log_write('info', 'result:')	
		log_write('info', res.decode('utf-8'))	
		log_write('info', ticket)
		ticket_dict = { "ticket" : ticket }
		httpres = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?' + urllib.urlencode(ticket_dict)
		log_write('info', httpres.decode('utf-8'))	
		return HttpResponse(httpres.decode('utf-8'))
