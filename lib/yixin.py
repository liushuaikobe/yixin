import hashlib
import time
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
		self.reply = Reply()
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
		if msgType == constant.TEXT_TYPE:
			if not self.textMsgBuilder:
				self.textMsgBuilder = messagebuilder.TextMsgBuilder(rawMsg)
			else:
				self.textMsgBuilder.setXmlStr(rawMsg)
			msg = self.textMsgBuilder.build()
		# TODO add msg type judgement
		callback(msgType, msg)
		return msg

	def replyText(self, toUser, fromUser, content=''):
		'''
		Wrpper for Reply Text message.
		'''
		return self.reply.replyText(toUser, fromUser, content)

	def getMsgType(self, rawMsg):
		root = ElementTree.fromstring(rawMsg.encode('utf-8'))
		return root.find(constant.MSG_TYPE_NODE_NAME).text

class Reply(object):
	'''
	Get the reply message.
	'''
	def __init__(self):
		pass

	def replyText(self, toUser, fromUser, content=''):
		args = ()
		return self.render(constant.REPLY_TEXT_TEMPLATE, (toUser, fromUser, self.getCurrentTime(), content))

	def getCurrentTime(self):
		return str(int(time.time()))

	def render(self, template, args):
		return template % tuple(args)


