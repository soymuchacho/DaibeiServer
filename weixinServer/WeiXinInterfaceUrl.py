#!/usr/bin/env python
# -*- coding: utf-8 -*-

WeiXinAppID = 'wx0120979b198dbf4f'
WeiXinSecret = '2baa626846df7b970935e572a29caab1'
LeShanPublishAppID = 'wx5fe2c07bcda0ec31'
LeShanPublishSecret = '8359a88aa655c0c7e9f47b26c05c9fdc'
SubscriptionAppID = 'wxb2cf9d8bfa9ac260'
SubscriptionSecret = '1325b7d7c31281932e38d868deef5c89'


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

# 获取用户信息
GetWeiXinUserInfoUrl = '/cgi-bin/user/info?'

# 获取微信全部资源列表
GetAllMaterialsUrl = '/cgi-bin/material/batchget_material?access_token='
