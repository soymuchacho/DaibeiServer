import redis
from logger import *

class ReisConnectMgr:
	def __init__(self):
		try:
			self.m_kRedisConnect = redis.StrictRedis(host="127.0.0.1", port=6379, db = 0)
			self.m_kRedisWebConnect = redis.StrictRedis(host="127.0.0.1", port=6379, db = 0)
			out_str = "connect redis 127.0.0.1 : 6379"
			log_write('info', out_str)

			self.m_kRedisPubsub = self.m_kRedisConnect.pubsub()
			self.m_kRedisWebPubsub = self.m_kRedisConnect.pubsub()
		except:	
			out_str = "cant connect redis 127.0.0.1 : 6379"
			log_write('info', out_str)


	def GetReisConnect(self):
		return self.m_kRedisConnect

	def GetRedisWebConnect(self):
		return self.m_kRedisWebConnect


	def GetReisPubsub(self):
		return self.m_kRedisPubsub

	def GetRedisWebPubsub(self):
		return self.m_kRedisWebPubsub

g_kRedisMgr = ReisConnectMgr()


