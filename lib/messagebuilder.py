# -*- coding: utf-8 -*-
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
			self.textMsg.meta[node.tag] = node.text
		return self.textMsg

class PicMsgBuilder(MsgBuilder):
	def __init__(self, xmlStr):
		MsgBuilder.__init__(self, xmlStr)
		self.picMsg = message.PicMsg()

	def build(self):
		root = ElementTree.fromstring(self.xmlStr)
		assert root.tag == 'xml'
		for node in root:
			self.picMsg.meta[node.tag] = node.text
		return self.picMsg

class LocationMsgBuilder(MsgBuilder):
	def __init__(self, xmlStr):
		MsgBuilder.__init__(self, xmlStr)
		self.locationMsg = message.LocationMsg()

	def build(self):
		root = ElementTree.fromstring(self.xmlStr)
		assert root.tag == 'xml'
		for node in root:
			self.locationMsg.meta[node.tag] = node.text
		return self.locationMsg
		
class EventMsgBuilder(MsgBuilder):
	def __init__(self, xmlStr):
		MsgBuilder.__init__(self, xmlStr)
		self.eventMsg = message.EventMsg()

	def build(self):
		root = ElementTree.fromstring(self.xmlStr)
		assert root.tag == 'xml'
		for node in root:
			self.eventMsg.meta[node.tag] = node.text
		return self.eventMsg
