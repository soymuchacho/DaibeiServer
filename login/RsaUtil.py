#coding=utf-8
import rsa
import base64

# 生成密钥
def RSAGenerateKey():
    (pubkey,privkey) = rsa.newkeys(1024)
    base64_pubkey = base64.encodestring(pubkey.save_pkcs1()) 
    base64_privkey = base64.encodestring(privkey.save_pkcs1()) 
    return base64_pubkey,base64_privkey 

# 私钥解密
def RSADecrypt(crypto,privkey):
    decode_privkey = base64.decodestring(privkey.load_pkcs1())
    message = rsa.decrypt(crypto,decode_privkey)
    return message


# base64解密
def Base64Decode(str):
    return base64.decodestring(str)

# base64加密
def Base64Encode(str):
    return base64.encodestring(str)


