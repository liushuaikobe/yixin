import logging
import os

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG

logging.basicConfig(filename='/home/dev-user/yixin_log.txt', level = logging.DEBUG, filemode = 'w', format = '%(asctime)s - %(levelname)s: %(message)s')  

def log(level, msg):
	if level == DEBUG:
		logging.debug(msg)
	elif level == INFO:
		logging.info(msg)
	elif level == WARNING:
		logging.warning(msg)
	elif level == ERROR:
		logging.error(msg)
	elif level == CRITICAL:
		logging.critical(msg)