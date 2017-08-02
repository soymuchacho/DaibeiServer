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

urlpatterns = [
    #url(r'^$',login_views.index,name='index'),
    url(r'^register$',login_views.Register,name='Register'),
    url(r'^advancelogin$',login_views.AdvanceLogin,name='advancelogin'),
    url(r'^login$',login_views.Authentication,name='authentication'),
    url(r'^download$',resource_views.Download_Resource,name='download'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^upload$',resource_views.Upload_Resource,name='upload'),
	url(r'^uploadhtml$',resource_views.uploadhtml),
]
