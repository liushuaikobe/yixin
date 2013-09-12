class Msg(object):
	'''
	Base class of messages posted from YiXin server.
	'''
	def __init__(self):
		meta = {
		'ToUserName' : '', # 1
		'FromUserName' : '', # 2
		'CreateTime' : '', # 3
		'MsgType' : '', # 4
		'MsgId' : '' # 5
	}

class TextMsg(Msg):
	'''
	Text messages.
	'''
	def __init__(self):
		Msg.__init__(self)
		self.meta.update({
				'Content' : '' # 6
			})
