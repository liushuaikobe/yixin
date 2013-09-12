# -*- coding: utf-8 -*-
import sys
sys.path.append('../../../lib')

from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode

import yixin
import constant

TOKEN = "lovezlp"

yixinApp = yixin.YiXin(TOKEN)

@csrf_exempt
def handleRequest(request):
	if request.method == 'GET':
		signature = request.GET.get("signature", None)
		timestamp = request.GET.get("timestamp", None)
		nonce = request.GET.get("nonce", None)
		echoStr = request.GET.get("echostr",None)
		return HttpResponse(yixinApp.checkSignature(signature, timestamp, nonce, echostr), content_type='text/plain')
	if request.method == 'POST':
		msg = yixinApp.handleMessage(request.raw_post_data)
		if msg.getMsgType() = constant.TEXT_TYPE: # we receive a text msg from some user
			yixinApp.replyText(msg.getFromUserName(), msg.getToUsername(), content=''.join((msg.getContent(), '\n----', 'Yours')))