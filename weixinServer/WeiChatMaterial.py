#coding=utf-8
from base.logger import *
from base.config_xml import *
from WeiXinInterfaceUrl import *
from WeiXinAccess import *
import ierror
import urllib
import urllib2
import json
import time

class Material():
	def __init__(self, mediaID, title, author, digest, picurl, url):
		self.mediaID = mediaID
		self.title = title
		self.author = author
		self.digest = digest
		self.picurl = picurl
		self.url = url
	
	def GetMediaID(self):
		return self.mediaID

	def GetTitle(self):
		return self.title

	def GetAuthor(self):
		return self.author

	def GetDigest(self):
		return self.digest

	def GetPicUrl(self):
		return self.picurl

	def GetUrl(self):
		return self.url



class WeiChatMaterialMgr():
	def __init__(self):
		self.VecMaterialsByTitle = {}
		self.VecMaterialsByID = {}
#		self.GetWeiChatAllMaterials("news")

	def AddMaterial(self, kMaterial):
		self.VecMaterialsByTitle[kMaterial.title] = kMaterial		# 以title做为主键
		self.VecMaterialsByID[kMaterial.title] = kMaterial			# 以ID做为主键
		out_str = 'AddMaterial : mediaID {0} title {1} author {2} url {3} picurl {4}'.format(kMaterial.GetMediaID(), 
				kMaterial.GetTitle().encode('utf-8'), kMaterial.GetAuthor().decode('utf-8'), kMaterial.GetUrl(), kMaterial.GetPicUrl())
		log_write('info', out_str)
		return True

	def GetMaterialByID(self, mediaID):
		kMaterial = self.VecMaterialsByID.get(mediaID)
		return kMaterial

	def GetMaterialByTitle(self, title):
		if self.VecMaterialsByTitle.has_key(title):
			return self.VecMaterialsByTitle.get(title)
		return None

	def DelMaterialByID(self, mediaID):
		if self.VecMaterialsByID.has_key(mediaID):
			del self.VecMaterialsByID[mediaID]

	def DelMaterialByTitle(self, title):
		if self.VecMaterialsByTitle.has_key(title):
			del self.VecMaterialsByTitle[title]

	def GetWeiChatAllMaterials(self, mediaType, offset = 0, count = 20):
		if WeiXinAccessSingleton.WeiXinAccessToken == '':
			WeiXinAccessSingleton.GetWeiXinAccess()

		i = 0
		while True:
			reqUrl = 'https://' + AccessPoint[0] + GetAllMaterialsUrl + WeiXinAccessSingleton.WeiXinAccessToken

			postData = ("{ \"type\": \"%s\", \"offset\": %d, \"count\": %d }"
					% (mediaType, offset, count))
			out_str = 'get weichat all Materials list : {0}'.format(reqUrl)
			log_write('info', out_str)

			res_data = urllib2.urlopen(reqUrl, postData)

			res = res_data.read()
			result = json.loads(res)
			out_str = 'recv weichat Materials list : {0}'.format(result)
			log_write('info', out_str)

			if result.has_key('errcode'):
				WeiXinAccessSingleton.GetWeiXinAccess()
				i = i + 1
			else:
				if result.has_key("item"):
					json_mater = result["item"]
					for i,val in enumerate(json_mater):
						if val.has_key("media_id"):
							mediaID = val["media_id"]
						else:
							continue

						if val.has_key("content"):
							if val["content"].has_key("news_item"):
								for j,news in enumerate(val["content"]["news_item"]):
									
									if news.has_key("thumb_media_id"):
										mediaID = news["thumb_media_id"]
									else:
										continue

									if news.has_key("title"):
										title = news["title"]
									else:
										continue

									if news.has_key("author"):
										author = news["author"]
									
									if news.has_key("digest"):
										digest = news["digest"]

									if news.has_key("url"):
										url = news["url"]

									if news.has_key("thumb_url"):
										picurl = news["thumb_url"]

									kMaterial = Material(mediaID, title, author, digest, picurl, url)
									self.AddMaterial(kMaterial)		
				break

			if i == 2:
				break;
		return True


	def Clear(self):
		self.VecMaterialsByID = {}
		self.VecMaterialsByTitle = {}

sWeiChatMaterialMgr = WeiChatMaterialMgr()


def GetBackMsg(qrcodeType, toUser, fromUser):
	out_str = 'GetBackMsg : qrcodeType {0} toUser {1} fromUser {2}'.format(qrcodeType, toUser, fromUser)
	log_write('info', out_str)
	info = sQrcodeInfoMgr.GetQrcodeInfo(qrcodeType)
	log_write(info, info)

	if info == None:
		log_write('info', 'cant find QrcodeInfo')
		return "success"

	kMaterial = sWeiChatMaterialMgr.GetMaterialByTitle(info.GetQrcodeRes())
	if kMaterial == None:
		log_write('info', 'qrcodeType Material is None')
		return "success"

	CreateTime = int(time.time()) 

	log_write('info', CreateTime)

	log_write('info', toUser)
	log_write('info', fromUser)
	log_write('info', str(CreateTime))
	log_write('info', kMaterial.GetTitle())
	log_write('info', kMaterial.GetAuthor())
	log_write('info', kMaterial.GetDigest())
	log_write('info', kMaterial.GetUrl())
	log_write('info', kMaterial.GetPicUrl())

	out_str = 'param : toUser {0} fromUser {1} CreateTime {2} Title {3} Description {4} PicUrl {5} Url {6} '.format(toUser, fromUser, str(CreateTime),
			kMaterial.GetTitle(), kMaterial.GetDigest(), kMaterial.GetPicUrl(), kMaterial.GetUrl())
	log_write('info', out_str)

	return_msg = '''<xml>
			<ToUserName>< ![CDATA[''' + toUser + '''] ]></ToUserName>
			<FromUserName>< ![CDATA[''' + fromUser + '''] ]></FromUserName>
			<CreateTime>''' + str(CreateTime) + '''</CreateTime>
			<MsgType>< ![CDATA[news] ]></MsgType>
			<ArticleCount>2</ArticleCount>
			<Articles>
			<item>
			<Title>< ![CDATA[''' + kMaterial.GetTitle().decode('utf-8') + '''] ]></Title> 
			<Description>< ![CDATA[''' + kMaterial.GetDigest().decode('utf-8') + '''] ]></Description>
			<PicUrl>< ![CDATA[''' + kMaterial.GetPicUrl().decode('utf-8') + '''] ]></PicUrl>
			<Url>< ![CDATA[''' + kMaterial.GetUrl().decode('utf-8') + '''] ]></Url>
			</item>
			</Articles>
			</xml>'''	

	out_str = 'return msg {0}'.format(return_msg)
	log_write('info', out_str)
	return return_msg
