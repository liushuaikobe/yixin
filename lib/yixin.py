import hashlib
from xml.etree import ElementTree

import utils 
import log
import constant
import messagebuilder

class YiXin(object):
	'''
	Main class of this lib.
	'''
	def __init__(self, token):
		self.token = token
		self.textMsgBuilder = None
		# TODO add builder

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

	def handleMessage(self, rawMsg, callback=None):
		'''
		Handle the message posted from YiXin Server.
		'''
		msgType = self.getMsgType(rawMsg)
		msg = None
		if msgType = constant.TEXT_TYPE:
			if not self.textMsgBuilder:
				self.textMsgBuilder = messagebuilder.TextMsgBuilder(rawMsg)
			else:
				self.textMsgBuilder.setXmlStr(rawMsg)
			msg = self.textMsgBuilder.build()
		# TODO add msg type judgement
		callback(msgType, msg)
		return msg

	# def reply()

	def getMsgType(rawMsg):
		return ElementTree.find(constant.MSG_TYPE_NODE_NAME).text

def main():
	'''
	Just for testing.
	'''
	y = YiXin('lvzlp')
	y.checkSignature('1', '1', '2',  7.99)

if __name__ == '__main__':
	main()

