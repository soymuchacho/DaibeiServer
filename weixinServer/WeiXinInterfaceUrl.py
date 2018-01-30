#!/usr/bin/env python
# -*- coding: utf-8 -*-

WeiXinAppID = 'wx0120979b198dbf4f'
WeiXinSecret = '2baa626846df7b970935e572a29caab1'

AccessPoint = { 
	0 : 'api.weixin.qq.com',			# 通用域名
	1 : 'sh.api.weixin.qq.com',			# 上海域名
	2 : 'sz.api.weixin.qq.com',			# 深圳域名
	3 : 'hk.api.weixin.qq.com'			# 香港域名
}

# 获取微信公众号的AccessToken
GetAccessTokenUrl = '/cgi-bin/token'

# 获取带参数的临时二维码
GetTemporaryQrCodeUrl = '/cgi-bin/qrcode/create?access_token='
