#!/usr/bin/env python
# -*- coding: utf-8 -*-
from WeiXinInterfaceUrl import *
import httplib
import urllib
import urllib2
import json
import ierror
from base.logger import *

class WeiXinAccess():
	WeiXinAccessToken = ''

	def GetWeiXinAccess(self):
		Url = "https://" + AccessPoint[0] + GetAccessTokenUrl + '?grant_type={0}&appid={1}&secret={2}';

		reqUrl = Url.format('client_credential', WeiXinAppID, WeiXinSecret)
		log_write('info', reqUrl)

		req = urllib2.Request(reqUrl)
		log_write('info', req)

		res_data = urllib2.urlopen(req)
		res = res_data.read()
		log_write('info', res)
	
		result = json.loads(res)
	
		if result.has_key("access_token"):
			self.WeiXinAccessToken = result["access_token"]
			log_write('info', self.WeiXinAccessToken)
			return ierror.WXInterfaceResult_OK

		return ierror.WXInterfaceResult_Failed;
			
WeiXinAccessSingleton = WeiXinAccess()
