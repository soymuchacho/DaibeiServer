#coding=utf-8
"""DaibeiServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from login import views as login_views
from resourceManager import views as resource_views
from weixinServer import views as weixin_views

urlpatterns = [
    #url(r'^$',login_views.index,name='index'),
    # 用户账号操作
	url(r'^register$',login_views.Register,name='Register'),
    #url(r'^advancelogin$',login_views.AdvanceLogin,name='advancelogin'),
    url(r'^login$',login_views.Authentication,name='authentication'),
	url(r'^resourcelist$',resource_views.GetUserResourceList,name='getuserresourcelist'),
	url(r'^resourcelist/version$',resource_views.GetUserResourceListVersion,name='getuserresourcelistversion'),
    url(r'^resource/download$',resource_views.Download_Resource,name='download'),
	# 管理员账号操作
	url(r'^admin$',login_views.AdminLogin,name='adminlogin'),
	url(r'^admin/register$',login_views.AdminRegister,name='AdminRegister'),
	#url(r'^admin/advancelogin$',login_views.AdminAdvanceLogin,name='AdminAdvanceLogin'),
	url(r'^admin/authentication$',login_views.AdminAuthentication,name='AdminAuthentication'),
	url(r'^admin/manager$',login_views.EnterManager,name='EnterManager'),
	url(r'^admin/manager/new/getuserlist$',login_views.GetAllUserList,name='GetAllUserList'),
	url(r'^admin/manager/new/getresourcelist$',resource_views.GetAllResource,name='GetAllResource'),
	url(r'^admin/manager/delete/resource$',resource_views.Delete_Resource,name='DeleteResource'),
	url(r'^upload$',resource_views.Upload_Resource,name='upload'),
	url(r'^uploadhtml$',resource_views.uploadhtml),
	# 后台数据库管理	
	url(r'^superadmin/', include(admin.site.urls)),
	# WebSocket
	url(r'^websocket/connect$', login_views.WebSocketConnect, name='WebSocketConnect'),
	url(r'.well-known/pki-validation/fileauth.txt$', login_views.CACheck, name='cacheck'),
	# 微信服务号
	url(r'weixinServer$', weixin_views.WeiXinCheck, name="weixincheck"),								# 微信消息获取
	url(r'weixinServer/getqrcode$', weixin_views.WeiXinGetQrCode, name='getqrcode'),						# 客户端获取带参数的二维码
]
