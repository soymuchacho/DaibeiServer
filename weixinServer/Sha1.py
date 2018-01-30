# -*- coding: utf-8 -*-
import sys
import hashlib
import ierror

class SHA1:
	def getSHA1(self, token, timestamp, nonce, encrypt):
		try:
			sortlist = [token, timestamp, nonce, encrypt]
			sortlist.sort()
			sha = hashlib.sha1()
			sha.update("".join(sortlist))
			return  ierror.WXBizMsgCrypt_OK, sha.hexdigest()
		except Exception,e:
			#print e
			return  ierror.WXBizMsgCrypt_ComputeSignature_Error, None
