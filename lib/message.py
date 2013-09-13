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
	Text messages.
	'''
	def __init__(self):
		Msg.__init__(self)
		self.meta.update({
				'Content' : '' # 6
			})
	def getContent(self):
		return self.meta['Content']
