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

from pymongo import MongoClient

import yixin
import constant
import log

TOKEN = 'lovezlp'
AppID = 'ca2c526a88744b5e98c0ac548de22725'
AppSecret = '0b331b59196141caa5dcb00df2f73fa9'

client = None
db = None
if not client:
	client = MongoClient('localhost', 27017)
	if not db:
		db = client.gitarchive

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
	global replyMsg, db
	yesterdayCollection = db.yesterday
	timelines = yesterdayCollection.find({'actor_attributes.login': msg.getContent()})
	count = timelines.count()
	if count < 1:
		count = 'no activity'
	elif count == 1:
		count = '1 activity'
	else:
		count = '%s activities' % count
	event = {}
	for timeline in timelines:
		if timeline['type'] in event:
			event[timeline['type']] += 1
		else:
			event[timeline['type']] = 1
	details = []
	for e in event:
		details.append('%s %s' % (e, event[e]))
	details = '\n'.join(tuple(details))

	replyMsg = yixinApp.replyText(msg.getFromUserName(), \
				msg.getToUsername(), \
				content='%s, you have %s yesterday.\n----\n%s' % (msg.getContent(), count, details))

yixinApp.setOnTextMsgReceivedCallback(receivedTextMsgCallback)
