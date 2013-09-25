# -*- coding: utf-8 -*-
import hashlib
import time
import simplejson
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
	def __init__(self, token, appId, appSecret):
		self.token = token
		self.appId = appId
		self.appSecret = appSecret

		self.accessToken = None
		self.accessTokenExpiresIn = None
		self.accessTokenGetTimeStamp = None

		self.reply = Reply()

		self.textMsgBuilder = None
		self.picMsgBuilder = None
		self.locationMsgBuilder = None
		self.eventMsgBuilder = None
		
		self.onTextMsgReceivedCallback = None
		self.onPicMsgReceivedCallback = None
		self.onLocationMsgReceivedCallback = None
		self.onEventMsgReceivedCallback = None
		self.onButtonClickCallback = None
		self.onUserSubscribeCallback = None
		self.onUserUnsbscribeCallback = None

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

	##     ##    ###    ##    ## ########  ##       ########         ##     ##  ######   ######   
	##     ##   ## ##   ###   ## ##     ## ##       ##               ###   ### ##    ## ##    ##  
	##     ##  ##   ##  ####  ## ##     ## ##       ##               #### #### ##       ##        
	######### ##     ## ## ## ## ##     ## ##       ######           ## ### ##  ######  ##   #### 
	##     ## ######### ##  #### ##     ## ##       ##               ##     ##       ## ##    ##  
	##     ## ##     ## ##   ### ##     ## ##       ##               ##     ## ##    ## ##    ##  
	##     ## ##     ## ##    ## ########  ######## ######## ####### ##     ##  ######   ######   

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
			if not self.locationMsgBuilder:
				self.locationMsgBuilder = messagebuilder.LocationMsgBuilder(rawMsg)
			else:
				self.locationMsgBuilder.setXmlStr(rawMsg)
			msg = self.locationMsgBuilder.build()
			if callable(self.onLocationMsgReceivedCallback):
				self.onLocationMsgReceivedCallback(msgType, msg)
		# we received a event push
		elif msgType == constant.EVENT_TYPE:
			if not self.eventMsgBuilder:
				self.eventMsgBuilder = messagebuilder.EventMsgBuilder(rawMsg)
			else:
				self.eventMsgBuilder.setXmlStr(rawMsg)
			msg = self.eventMsgBuilder.build()
			if callable(self.onEventMsgReceivedCallback):
				self.onEventMsgReceivedCallback(msgType, msg)
			# dispatch the specific event
			event = msg.getEvent().lower()
			# new subscribe
			if event == constant.SUBSCRIBE_EVENT:
				if callable(self.onUserSubscribeCallback):
					self.onUserSubscribeCallback(msgType, msg)
			# new unsubscribe
			elif event == constant.UNSUBSCRIBE_EVENT:
				if callable(self.onUserUnsbscribeCallback):
					self.onUserUnsbscribeCallback(msgType, msg)
			# button clicked
			elif event == constant.CLICK_EVETN:
				if callable(self.onButtonClickCallback):
					self.onButtonClickCallback(msgType, msg)

		if callable(callback):
			callback(msgType, msg)
		return msg

	########  ######## ########  ##       ##    ## 
	##     ## ##       ##     ## ##        ##  ##  
	##     ## ##       ##     ## ##         ####   
	########  ######   ########  ##          ##    
	##   ##   ##       ##        ##          ##    
	##    ##  ##       ##        ##          ##    
	##     ## ######## ##        ########    ##   

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
		root = etree.fromstring(rawMsg)
		return root.find(constant.MSG_TYPE_NODE_NAME).text

	 ######     ###    ##       ##       ########     ###     ######  ##    ## 
	##    ##   ## ##   ##       ##       ##     ##   ## ##   ##    ## ##   ##  
	##        ##   ##  ##       ##       ##     ##  ##   ##  ##       ##  ##   
	##       ##     ## ##       ##       ########  ##     ## ##       #####    
	##       ######### ##       ##       ##     ## ######### ##       ##  ##   
	##    ## ##     ## ##       ##       ##     ## ##     ## ##    ## ##   ##  
	 ######  ##     ## ######## ######## ########  ##     ##  ######  ##    ## 

	def setOnTextMsgReceivedCallback(self, callback):
		assert callable(callback)
		self.onTextMsgReceivedCallback = callback

	def setOnPicMsgReceivedCallback(self, callback):
		assert callable(callback)
		self.onPicMsgReceivedCallback = callback

	def setOnLocationMsgReceivedCallback(self, callback):
		assert callable(callback)
		self.onLocationMsgReceivedCallback = callback

	def setOnEventMsgReceivedCallback(self, callback):
		assert callable(callback)
		self.onEventMsgReceivedCallback = callback

	def setOnButtonClickCallback(self, callback):
		assert callable(callback)
		self.onButtonClickCallback = callback

	def setOnUserSubscribeCallback(self, callback):
		assert callable(callback)
		self.onUserSubscribeCallback = callback

	def setOnUserUnsbscribeCallback(self, callback):
		assert callable(callback)
		self.onUserUnsbscribeCallback = callback

	def getAccessToken(self):
		if self.accessToken and self.accessTokenExpiresIn and self.accessTokenGetTimeStamp: # We have got the access token.
			if time.time() - self.accessTokenGetTimeStamp < self.accessTokenExpiresIn: # The access token is valid until now.
				log.log(log.DEBUG, self.accessToken + '  old')
				return self.accessToken
		url = constant.GET_TOKEN_URL
		params = {
			'grant_type' : 'client_credential',
			'appid' : self.appId,
			'secret' : self.appSecret
		}
		result = simplejson.loads(utils.doGet(url, params))
		self.accessToken = result['access_token']
		self.accessTokenExpiresIn = float(result['expires_in'])
		self.accessTokenGetTimeStamp = time.time()
		log.log(log.DEBUG, self.accessToken + '  new')
		return self.accessToken

	##     ## ######## ##    ## ##     ## 
	###   ### ##       ###   ## ##     ## 
	#### #### ##       ####  ## ##     ## 
	## ### ## ######   ## ## ## ##     ## 
	##     ## ##       ##  #### ##     ## 
	##     ## ##       ##   ### ##     ## 
	##     ## ######## ##    ##  #######  

	def addMenu(self, buttonGroup):
		log.log(log.DEBUG, simplejson.dumps(buttonGroup.meta))
		utils.doPostWithoutParamsEncoding(''.join((constant.ADD_MENU_URL, self.getAccessToken())), \
			simplejson.dumps(buttonGroup.meta))

	def deleteMenu(self):
		'''
		Delete the menu.
		'''
		log.log(log.DEBUG, 'Delete menu.')
		params = {
			'access_token' : self.getAccessToken()
		}
		result = utils.doGet(constant.DELETE_MENU_URL, params)
		log.log(log.DEBUG, result)

	def queryCurrentMenu(self):
		'''
		Get the current structure of the menu.
		'''
		pass



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

class Button(object):
	'''
	Base class of the Menu Button.
	'''
	CLICK_TYPE = 'click'
	def __init__(self):
		self.meta = {
			'name' : '',
		}

	def setName(self, name):
		self.meta['name'] = name

class CommonClickButton(Button):
	'''
	 A common click-type Button including name and type and key.
	'''
	def __init__(self):
		Button.__init__(self)
		self.meta.update({
				'type' : Button.CLICK_TYPE,
				'key' : ''
			})

	def setKey(self, key):
		self.meta['key'] = key

class TopLevelButton(Button):
	'''
	A top level button than contains some sub-buttons.
	'''
	def __init__(self):
		Button.__init__(self)
		self.meta.update({
				'sub_button' : []
			})

	def addSubButton(self, commonButton):
		self.meta['sub_button'].append(commonButton.meta)

class ButtonGroup(object):
	'''
	A group of buttons.
	'''
	def __init__(self):
		self.meta = {
			'button' : []
		}

	def addButton(self, button):
		self.meta['button'].append(button.meta)
