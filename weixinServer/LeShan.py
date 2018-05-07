#!/usr/bin/env python
# -*- coding: utf-8 -*-
from WeiXinInterfaceUrl import *
import httplib
import urllib
import urllib2
import json
import ierror
from base.logger import *

class LeShanPublishAccess():
	LeShanPublishAccessToken = ''

	def GetWeiXinAccess(self):
		log_write('info', 'LeShanPublishAccess')
		Url = "https://" + AccessPoint[0] + GetAccessTokenUrl + '?grant_type={0}&appid={1}&secret={2}';

		reqUrl = Url.format('client_credential', LeShanPublishAppID, LeShanPublishSecret)
		log_write('info', reqUrl)

		req = urllib2.Request(reqUrl)
		log_write('info', req)

		res_data = urllib2.urlopen(req)
		res = res_data.read()
		log_write('info', res)
	
		result = json.loads(res)
	
		if result.has_key("access_token"):
			self.LeShanPublishAccessToken = result["access_token"]
			log_write('info', self.LeShanPublishAccessToken)
			return ierror.WXInterfaceResult_OK

		return ierror.WXInterfaceResult_Failed;
			

LeShanPublishAccessSingleton = LeShanPublishAccess()
