#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from .RsaUtil import *
from django.core.cache import cache
from base.logger import *
from base.defines import *
import time
import httplib

# 登陆界面
def index(request):
    log_write('info','载入index界面')
    return render(request,'index.html')

# 帐号注册
def Register(request):
    if request.method == 'POST':
        username = request.GET.get('username')
        password = request.GET.get('password')
        # 位置
        location = request.GET.get('location')
        log_write('info','用户开始注册 %s %s %s',username,password,location)
        # 生成token md5(base64(用户名+密钥+当前时间))
        now_time = time.localtime(time.time())
        m2 = hashlib.md5()
        m2.update(Base64Encode(username+token_secretkey+now_time));
        token = m2.hexdigest()

        log_write('info','生成token %s ',token)
        # 先查询数据库用户是否已经存在
        old_user = models.User_Info.objects.get(username=username)
        if old_user != None:
            return HttpResponse("{'code' : '308', 'msg' : 'user exist'}")
        # 用户不存在，创建
        new_user = models.User_Info(username=username,password=password,token=token,location=location)
        if new_user == None:
            return HttpResponse("{'code' : '404','msg':'user register error'}")
        new_user.save()
        log_write('info','帐号注册成功')
        return HttpResponse("{'code':'200','msg' : 'ok'}")
    else:
        return HttpResponse("{'error' : 'request post '}")

# GET方式预登陆
def AdvanceLogin(request):
    if request.method == 'GET':
        # 返回公钥
        (pubkey,privkey) = RSAGenerateKey()
        username = request.GET.get('username')
        # 先查看缓存中用户是否存在
        user = cache.get(username=username)
        if user == None:
            user = Models.User_Info.objects.get(username)
            if user == None:
                return HttpResponse("{'error' : 'user not exist'}")

        # 将私钥保存
        user.privtekey = privkey
        user.publickey = pubkey
        # 更新数据库
        models.User_Info.objects.filter(username=username).update(privtekey=privkey,publickey=pubkey)
        # 保存到缓存中
        cache.set(username,user,0)
        log_write('info','user advance login : %s',username)
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
           
            decode_username = Base64Decode(username)
            decode_password = Base64Decode(password)
            
            #获取私钥
            privkey = cache.get(username)
            
            rsadecode_username = RSADecrypt(decode_username,privkey)
            rsadecode_password = RSADecrypt(decode_password,privkey)

            log_write('info','user Authenticationtion : %s %s',rsadecode_username,rsadecode_password)
           
            # 检测帐号
            user = models.User_Info.objects.get(username=rsadecode_username)
            user.privtekey = privkey
            if rsadecode_password == user.password:
                result = "{'token':%s}" % user.token
                cache.set(username,user,0)
                return HttpResponse(result)
            else:
                return HttpResponse("{'error':'username or password error'}")
    else:
        form = LoginForm()
    return render(request,'index.html',{'form',form}) 
