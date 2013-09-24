# -*- coding: utf-8 -*-
import types
import urllib
import urllib2

def checkType(isType=type(''), *arg):
	if len(arg) == 0:
		return False
	for a in arg:
		if type(a) != isType:
			return False
	return True

def doGet(url, params):
	'''
	Make a HTTP GET request.
	'''
	params = urllib.urlencode(params)
	req = urllib2.Request(url='%s?%s' % (url, params))
	result = urllib2.urlopen(req).read()
	return result

def doPostWithoutParamsEncoding(url, params):
	'''
	Make a HTTP POST request
	NOTICE : the params of the post request WON'T be encoded by urllib.urlencode
	'''
	req = urllib2.Request(url=url, data=params)
	result = urllib2.urlopen(req).read()
	return result