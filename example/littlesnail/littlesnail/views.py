# -*- coding: utf-8 -*-
import sys
libpath = '/home/dev-user/djangoapp/yixin/lib'
# libpath = '/Users/liushuai/git/PythonProject/yixin/lib'
if libpath not in sys.path:
	sys.path.append(libpath)
print sys.path

from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode

import yixin
import constant
import log

TOKEN = 'lovezlp'
AppID = 'ca2c526a88744b5e98c0ac548de22725'
AppSecret = '0b331b59196141caa5dcb00df2f73fa9'

yixinApp = yixin.YiXin(TOKEN, AppID, AppSecret)

replyMsg = None

@csrf_exempt
def handleRequest(request):
	log.log(log.INFO, 'reveive request')

	if request.method == 'GET':
		log.log(log.INFO, 'GET')

		# content get from request.GET is a Unicode object, we should change it to a object of string.
		signature = request.GET.get("signature", None).encode('utf-8')
		timestamp = request.GET.get("timestamp", None).encode('utf-8')
		nonce = request.GET.get("nonce", None).encode('utf-8')
		echoStr = request.GET.get("echostr",None).encode('utf-8')

		log.log(log.INFO, ''.join((signature, ' ', timestamp, ' ', nonce, ' ', echoStr)))

		return HttpResponse(yixinApp.checkSignature(signature, timestamp, nonce, echoStr), content_type='text/plain')

	if request.method == 'POST':
		yixinApp.handleMessage(request.raw_post_data)
		return HttpResponse(replyMsg, content_type='application/xml')

def receivedTextMsgCallback(msgType, msg):
	global replyMsg
	if msg.getContent() == 'music':
		replyMsg = yixinApp.replyMusic(msg.getFromUserName(), msg.getToUsername(), 'Every Moment Of My Life', 'very nice~', 'http://219.217.227.89/test.mp3', 'http://219.217.227.89/test.mp3')
	elif msg.getContent() == 'news':
		article1 = yixin.Article()
		article1.setTitle('Test News')
		article1.setDescription('Every moment of My Life.')
		article1.setPicUrl('http://219.217.227.89/1.jpeg')
		article1.setUrl('http://219.217.227.89/index.html')

		article2 = yixin.Article()
		article2.setTitle('Test News too')
		article2.setDescription('Need you now.')
		article2.setPicUrl('http://219.217.227.89/2.jpeg')
		article2.setUrl('http://219.217.227.89/index.html')

		artiles = [article1, article2]

		replyMsg = yixinApp.replyNews(msg.getFromUserName(), msg.getToUsername(), 2, artiles)
	elif msg.getContent() == 'add':
		buttonGroup = yixin.ButtonGroup()

		btn1 = yixin.CommonClickButton()
		btn1.setName('kobe')
		btn1.setKey('btn1')

		btn2 = yixin.CommonClickButton()
		btn2.setName('wade')
		btn2.setKey('btn2')

		btn3 = yixin.TopLevelButton()
		btn3.setName('test subbtn')

		subBtn1 = yixin.CommonClickButton()
		subBtn1.setName('james')
		subBtn1.setKey('subbtn1')

		subBtn2 = yixin.CommonClickButton()
		subBtn2.setName('bosh')
		subBtn2.setKey('subbtn2')

		btn3.addSubButton(subBtn1)
		btn3.addSubButton(subBtn2)

		buttonGroup.addButton(btn1)
		buttonGroup.addButton(btn2)
		buttonGroup.addButton(btn3)

		yixinApp.addMenu(buttonGroup)
	elif msg.getContent() == 'delete':
		yixinApp.deleteMenu()
		replyMsg = yixinApp.replyText(msg.getFromUserName(), msg.getToUsername(), content='Delete successful')
	else:
		replyMsg = yixinApp.replyText(msg.getFromUserName(), msg.getToUsername(), content=''.join((msg.getContent(), '\n----\n', 'Yours')))

def receivedPicMsgCallback(msgType, msg):
	global replyMsg
	replyMsg = yixinApp.replyText(msg.getFromUserName(), msg.getToUsername(), content=''.join((msg.getPicUrl(), '\n----\n', 'Your Pic')))

def receivedLocationMsgCallback(msgType, msg):
	global replyMsg
	replyMsg = yixinApp.replyText(msg.getFromUserName(), msg.getToUsername(), content=''.join((msg.getLocation_X(), '\n', msg.getLocation_Y(), '\n', msg.getScale(), '\n', msg.getLabel())))

def receivedEventMsgCallback(msgType, msg):
	global replyMsg
	replyMsg = yixinApp.replyText(msg.getFromUserName(), msg.getToUsername(), content=''.join((msg.getEvent(), '\n', msg.getEventKey())))


yixinApp.setOnTextMsgReceivedCallback(receivedTextMsgCallback)
yixinApp.setOnPicMsgReceivedCallback(receivedPicMsgCallback)
yixinApp.setOnLocationMsgReceivedCallback(receivedLocationMsgCallback)
yixinApp.setOnEventMsgReceivedCallback(receivedEventMsgCallback)
