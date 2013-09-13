import message

from xml.etree import ElementTree

class MsgBuilder(object):
	'''
	Generate a message object from the xml string.
	'''
	def __init__(self, xmlStr):
		self.xmlStr = xmlStr

	def build(self):
		raise NotImplementedError

	def setXmlStr(self, xmlStr):
		self.xmlStr = xmlStr

class TextMsgBuilder(MsgBuilder):
	def __init__(self, xmlStr):
		MsgBuilder.__init__(self, xmlStr)
		self.textMsg = message.TextMsg()

	def build(self):
		root = ElementTree.fromstring(self.xmlStr)
		assert root.tag == 'xml'
		for node in root:
			self.textMsg.meta[node.tag] = unicode(node.text, 'utf-8')
		return self.textMsg

class PicMsgBuilder(MsgBuilder):
	def __init__(self, xmlStr):
		MsgBuilder.__init__(self, xmlStr)
		self.picMsg = message.PicMsg()

	def build(self):
		root = ElementTree.fromstring(self.xmlStr)
		assert root.tag == 'xml'
		for node in root:
			self.picMsg.meta[node.tag] = unicode(node.text, 'utf-8')
		return self.picMsg
		
