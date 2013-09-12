import hashlib

import utils 
import log

class YiXin(object):
	'''
	Main class of this lib.
	'''
	def __init__(self, token):
		self.token = token

	def checkSignature(self, signature, timestamp, nonce, echostr):
		'''
		check the signature, 
		'''
		if not utils.checkType(type(''), signature, timestamp, nonce, echostr):
			log.log(log.ERROR, 'Your args for signature checking must be ' + str(type('')))
			return None
		tmpLst = [self.token, timestamp, nonce]
		tmpLst.sort()
		tmpStr = ''.join(tuple(tmpLst))
		tmpStr = hashlib.sha1(tmpStr).hexdigest()
		if tmpStr == signature:
			log.log(log.INFO, 'Signature checking successfully.')
			return echostr
		else:
			log.log(log.ERROR, 'Signature checking failed.')
			return None

def main():
	'''
	Just for testing.
	'''
	y = YiXin('lvzlp')
	y.checkSignature('1', '1', '2',  7.99)

if __name__ == '__main__':
	main()

