#coding=utf-8
import logging

logger = logging.getLogger("DaibeiServer.custom")

def log_write(level,data):
	try:
		if level == 'debug':
			logger.debug(data)
		elif level == 'info':
			logger.info(data)
		elif level == 'error':
			logger.error(data)
		elif level == 'warning':
			logger.warning(data)
		else:
			logger.critical(data)
	except:
		return None
	return None
