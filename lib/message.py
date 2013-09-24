# -*- coding: utf-8 -*-

class Msg(object):
	'''
	Base class of messages posted from YiXin server.
	'''
	def __init__(self):
		self.meta = {
		'ToUserName' : '', # 1
		'FromUserName' : '', # 2
		'CreateTime' : '', # 3
		'MsgType' : '', # 4
		'MsgId' : '' # 5
	}

	def getToUsername(self):
		return self.meta['ToUserName']

	def getFromUserName(self):
		return self.meta['FromUserName']

	def getCreateTime(self):
		return self.meta['CreateTime']

	def getMsgType(self):
		return self.meta['MsgType']

	def getMsgId(self):
		return self.meta['MsgId']

class TextMsg(Msg):
	'''
	Text message.
	'''
	def __init__(self):
		Msg.__init__(self)
		self.meta.update({
				'Content' : '' # 6
			})
	def getContent(self):
		return self.meta['Content']

class PicMsg(Msg):
	'''
	Picture message.
	'''
	def __init__(self):
		Msg.__init__(self)
		self.meta.update({
				'PicUrl' : '' # 6
			})

	def getPicUrl(self):
		return self.meta['PicUrl']

class LocationMsg(Msg):
	'''
	Location message.
	'''
	def __init__(self):
		Msg.__init__(self)
		self.meta.update({
				'Location_X' : '', # 6
				'Location_Y' : '', # 7
				'Scale' : '', # 8
				'Label' : '' # 9
			})

	def getLocation_X(self):
		return self.meta['Location_X']

	def getLocation_Y(self):
		return self.meta['Location_Y']

	def getScale(self):
		return self.meta['Scale']

	def getLabel(self):
		return self.meta['Label']

class EventMsg(Msg):
	'''
	Event Push.
	NOTICE : This kind of message doesn't contain MsgId tag.
	'''
	def __init__(self):
		Msg.__init__(self)
		self.meta.update({
				'Event' : '', # 6
				'EventKey' : '' # 7
			})

	def getEvent(self):
		return self.meta['Event']

	def getEventKey(self):
		return self.meta['EventKey']
