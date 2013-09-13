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
		self.picMsgBuilder = None
		# TODO add builder
		self.onTextMsgReceivedCallback = None
		self.onPicMsgReceivedCallback = None

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
		# we received a text message
		if msgType == constant.TEXT_TYPE:
			if not self.textMsgBuilder:
				self.textMsgBuilder = messagebuilder.TextMsgBuilder(rawMsg)
			else:
				self.textMsgBuilder.setXmlStr(rawMsg)
			msg = self.textMsgBuilder.build()
			self.onTextMsgReceivedCallback(msgType, msg)
		# we received a image message
		elif msgType == constant.PIC_TYPE:
			if not self.picMsgBuilder:
				self.picMsgBuilder = messagebuilder.PicMsgBuilder(rawMsg)
			else:
				self.picMsgBuilder.setXmlStr(rawMsg)
			msg = self.picMsgBuilder.build()
			self.onPicMsgReceivedCallback(msgType, msg)
		# TODO add msg type judgement
		if callable(callback):
			callback(msgType, msg)
		return msg

	def replyText(self, toUser, fromUser, content=''):
		'''
		Wrpper for replying text message.
		'''
		return self.reply.replyText(toUser, fromUser, content)

	def replyMusic(self, toUser, fromUser, title, description, musicUrl, HQMusicUrl):
		'''
		Wrapper for replying music message.
		'''
		return self.reply.replyMusic(toUser, fromUser, title, description, musicUrl, HQMusicUrl)

	def getMsgType(self, rawMsg):
		root = ElementTree.fromstring(rawMsg.encode('utf-8'))
		return root.find(constant.MSG_TYPE_NODE_NAME).text

	def setOnTextMsgReceivedCallback(self, callback):
		assert callable(callback)
		self.onTextMsgReceivedCallback = callback

	def setOnPicMsgReceivedCallback(self, callback):
		assert callable(callback)
		self.onPicMsgReceivedCallback = callback

class Reply(object):
	'''
	Get the reply message.
	'''
	def __init__(self):
		pass

	def replyText(self, toUser, fromUser, content=''):
		return self.render(constant.REPLY_TEXT_TEMPLATE, (toUser, fromUser, self.getCurrentTime(), content))

	def replyMusic(self, toUser, fromUser, title, description, musicUrl, HQMusicUrl):
		return self.render(constant.REPLY_MUSIC_TEMPLATE, (toUser, fromUser, self.getCurrentTime(), title, description, musicUrl, HQMusicUrl))

	def getCurrentTime(self):
		return str(int(time.time()))

	def render(self, template, args):
		return template % tuple(args)


