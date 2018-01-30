# -*- coding: utf-8 -*-
import base64
import string
import random
import hashlib
import time
import struct
import xml.etree.cElementTree as ET
import sys
import socket
reload(sys)
import ierror
sys.setdefaultencoding('utf-8')

class XMLParse:
	"""提供提取消息格式中的密文及生成回复消息格式的接口"""

	# xml消息模板
	AES_TEXT_RESPONSE_TEMPLATE = """<xml>
		<Encrypt><![CDATA[%(msg_encrypt)s]]></Encrypt>
		<MsgSignature><![CDATA[%(msg_signaturet)s]]></MsgSignature>
		<TimeStamp>%(timestamp)s</TimeStamp>
		<Nonce><![CDATA[%(nonce)s]]></Nonce>
		</xml>"""

	def extract(self, xmltext):
		"""提取出xml数据包中的加密消息
			@param xmltext: 待提取的xml字符串
			@return: 提取出的加密消息字符串
		"""
		try:
			xml_tree = ET.fromstring(xmltext)
			encrypt  = xml_tree.find("Encrypt")
			touser_name    = xml_tree.find("ToUserName")
			return  ierror.WXBizMsgCrypt_OK, encrypt.text, touser_name.text
		except Exception,e:
			#print e
			return  ierror.WXBizMsgCrypt_ParseXml_Error,None,None

	def generate(self, encrypt, signature, timestamp, nonce):
		"""生成xml消息
		@param encrypt: 加密后的消息密文
		@param signature: 安全签名
		@param timestamp: 时间戳
		@param nonce: 随机字符串
		@return: 生成的xml字符串	
		"""
		resp_dict = {
			'msg_encrypt' : encrypt,
			'msg_signaturet': signature,
			'timestamp'    : timestamp,
			'nonce'        : nonce,	
			}
			
		resp_xml = self.AES_TEXT_RESPONSE_TEMPLATE % resp_dict
		return resp_xml
