import logging
import os

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG

# filename = '/Users/liushuai/yixin_log.txt'
filename = '/home/dev-user/yixin_log.txt'
logging.basicConfig(filename=filename, level = logging.DEBUG, filemode = 'a', format = '%(asctime)s - %(levelname)s: %(message)s')  

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