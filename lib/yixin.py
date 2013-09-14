import hashlib
import time
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element, SubElement, ElementTree

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
		self.locationBuilder = None
		# TODO add builder
		self.onTextMsgReceivedCallback = None
		self.onPicMsgReceivedCallback = None
		self.onLocationMsgReceivedCallback = None

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
			if callable(self.onTextMsgReceivedCallback):
				self.onTextMsgReceivedCallback(msgType, msg)
		# we received a image message
		elif msgType == constant.PIC_TYPE:
			if not self.picMsgBuilder:
				self.picMsgBuilder = messagebuilder.PicMsgBuilder(rawMsg)
			else:
				self.picMsgBuilder.setXmlStr(rawMsg)
			msg = self.picMsgBuilder.build()
			if callable(self.onPicMsgReceivedCallback):
				self.onPicMsgReceivedCallback(msgType, msg)
		# we received a image message
		elif msgType == constant.LOCATION_TYPE:
			if not self.locationBuilder:
				self.locationBuilder = messagebuilder.LocationMsgBuilder(rawMsg)
			else:
				self.locationBuilder.setXmlStr(rawMsg)
			msg = self.locationBuilder.build()
			if callable(self.onLocationMsgReceivedCallback):
				self.onLocationMsgReceivedCallback(msgType, msg)
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

	def replyNews(self, toUser, fromUser, articleCount, articles):
		'''
		Wrapper for replying news message.
		'''
		return self.reply.replyNews(toUser, fromUser, articleCount, articles)

	def getMsgType(self, rawMsg):
		root = etree.fromstring(rawMsg.encode('utf-8'))
		return root.find(constant.MSG_TYPE_NODE_NAME).text

	def setOnTextMsgReceivedCallback(self, callback):
		assert callable(callback)
		self.onTextMsgReceivedCallback = callback

	def setOnPicMsgReceivedCallback(self, callback):
		assert callable(callback)
		self.onPicMsgReceivedCallback = callback

	def setOnLocationMsgReceivedCallback(self, callback):
		assert callable(callback)
		self.onLocationMsgReceivedCallback = callback

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

	def replyNews(self, toUser, fromUser, articleCount, articles):
		root = Element(Article.ROOT_TAG_NAME)
		for artile in articles:
			item = SubElement(root, Article.ITEM_TAG_NAME)
			for tag in artile.meta:
				subElement = SubElement(item, tag)
				subElement.text = str(artile.meta[tag])
		return self.render(constant.REPLY_NEWS_TEMPLATE, (toUser, fromUser, self.getCurrentTime(), str(articleCount), etree.tostring(root)))

	def getCurrentTime(self):
		return str(int(time.time()))

	def render(self, template, args):
		return template % tuple(args)

class Article(object):
	'''
	Sub nodes of News type message that reply to the user.
	NOTICE : the object of this class is used for replying to the user rather than being built from received message.
	'''
	ROOT_TAG_NAME = 'Articles'
	ITEM_TAG_NAME = 'item'
	def __init__(self):
		self.meta = {
			'Title' : '',
			'Description' : '',
			'PicUrl' : '',
			'Url' : ''
		}

	def setTitle(self, title):
		self.meta['Title'] = title

	def setDescription(self, description):
		self.meta['Description'] = description

	def setPicUrl(self, picUrl):
		self.meta['PicUrl'] = picUrl

	def setUrl(self, url):
		self.meta['Url'] = url

