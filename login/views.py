#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from .RsaUtil import *
from django.core.cache import cache
from base.logger import *
from base.defines import *
import time
import hashlib
from login.models import User_Info

token_secretkey = "1qaz@WSX3edc$RFV5tgb^YHN7ujm*IK<0p;/"

# 登陆界面
#def index(request):
#    log_write('info','载入index界面')
#    return render(request,'index.html')

# 帐号注册
def Register(request):
	if request.method == 'POST':
		print request.POST;
		username = request.POST.get('username').encode('utf-8')
		password = request.POST.get('password').encode('utf-8')
		location = request.POST.get('location').encode('utf-8')
		log_write('info','post数据 %s %s %s',username,password,location)
		log_write('info','开始注册')	
		# 进行解密	
		username_decode = Base64Decode(username)
		if username_decode == None:
			log_write('info','用户名解密失败')	
			return HttpResponse("{'error':'username decode error'}")
		password_decode = Base64Decode(password)
		if password_decode == None:
			log_write('info','密码解密失败')	
			return HttpResponse("{'error':'password decode error'}")
		location_decode = Base64Decode(location)	
		if location_decode == None:
			log_write('info','地址解密失败')	
			return HttpResponse("{'error':'location decode error'}")
		log_write('info','解密完成')	
		log_write('info','用户开始注册 %s %s %s',username_decode,password_decode,location_decode)

		# 生成token md5(base64(用户名+密钥+当前时间))
		now_time = time.strftime("%Y-%02m-%02d %02H:%02M:%02S",time.localtime(time.time()))
		encode_str = Base64Encode(username_decode+token_secretkey+now_time)
		m2 = hashlib.md5()
		m2.update(encode_str)
		token = m2.hexdigest().encode('utf-8')
		log_write('info','生成token %s ',token)

		# 先查询数据库用户是否已经存在
		old_user = User_Info.objects.filter(username=username_decode)
		print old_user
		print len(old_user)
		if len(old_user) != 0:
			log_write('info','用户%s已存在,注册失败',username_decode)
			return HttpResponse("{'code' : '308', 'msg' : 'user exist'}")
		log_write('info','用户不存在，可以注册')
		# 用户不存在，创建
		new_user = User_Info(username=username_decode,password=password_decode,token=token,location=location_decode)
		if new_user == None:
			return HttpResponse("{'error':'register error'}")
		new_user.save()
		log_write('info','帐号注册成功')
		return HttpResponse("{'code':'200','msg' : 'ok'}")
	else:
		return HttpResponse("{'error' : 'request post '}")

# GET方式预登陆
def AdvanceLogin(request):
    if request.method == 'POST':
        # 返回公钥
        (pubkey,privkey) = RSAGenerateKey()
        username = request.POST.get('username')
        
	# base64
	username = Base64Decode(username)
	log_write('info','用户%s进行预登陆',username)

	# 先查看缓存中用户是否存在
        user = cache.get(username)
        print user
	if user == None:
            user = User_Info.objects.filter(username=username)
	    if len(user) == 0:
                return HttpResponse("{'error' : 'user not exist'}")

        # 将私钥保存
        user.privtekey = privkey
        user.publickey = pubkey
        # 更新数据库
        User_Info.objects.filter(username=username).update(privtekey=privkey,publickey=pubkey)
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
		username = request.POST.get('username')
		password = request.POST.get('password')

		decode_username = Base64Decode(username)
		decode_password = Base64Decode(password)

		#获取私钥
		privkey = cache.get(username)

		rsadecode_username = RSADecrypt(decode_username,privkey)
		rsadecode_password = RSADecrypt(decode_password,privkey)

		log_write('info','user Authenticationtion : %s %s',rsadecode_username,rsadecode_password)

		# 检测帐号
		user = User_Info.objects.filter(username=rsadecode_username)
		if len(user) == 0:
			return HttpResponse("{'error':'username or password error'}")
		user.privtekey = privkey
		if rsadecode_password == user.password:
			result = "{'token':%s}" % user.token
			# 以username为key设置一个缓存，再以token为key设置一个token对应的username
			cache.set(username,user,0)
			cache.set(user.token,username,0)
			return HttpResponse(result)
		else:
			return HttpResponse("{'error':'username or password error'}")
	else:
		return HttpResponse("{'error':'badmethod'}") 
