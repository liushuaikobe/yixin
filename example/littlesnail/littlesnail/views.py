# -*- coding: utf-8 -*-
import sys
libpath = '/home/dev-user/djangoapp/yixin/lib'
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

TOKEN = "lovezlp"

yixinApp = yixin.YiXin(TOKEN)

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
		msg = yixinApp.handleMessage(request.raw_post_data)

		if msg.getMsgType() == constant.TEXT_TYPE: # we receive a text msg from some user
			replyMsg = yixinApp.replyText(msg.getFromUserName(), msg.getToUsername(), content=''.join((msg.getContent(), '\n----\n', 'Yours')))
			
		return HttpResponse(replyMsg, content_type='application/xml')