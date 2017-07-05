#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from .RsaUtil import *
from django.core.cache import cache

# Create your views here.

# 登陆界面
def index(request):
    return render(request,'index.html')

# GET方式预登陆
def AdvanceLogin(request):
    if request.method == 'GET':
        # 返回公钥
        (pubkey,privkey) = RSAGenerateKey()
        username = request.GET.get('username')
        # 将私钥保存
        cache.set(username,"{'123':'245'}",2*24*3600)
        # 返回公钥
        response = "{'publickey' : '%s'}" % pubkey
        return HttpResponse(response)
    else:
        return HttpResponse("{'error' : 'Bad Method'}")
# 帐号验证
def Authentication(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #获取私钥
            #privkey = cache.get(username)
            print username,password
            return HttpResponse("login successful")
    else:
        form = LoginForm()
    return render(request,'index.html',{'form',form}) 
