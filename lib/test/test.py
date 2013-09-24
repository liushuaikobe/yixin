# -*- coding: utf-8 -*-
from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element, SubElement, ElementTree
import urllib
import urllib2
import simplejson

msg = '<xml> <ToUserName><![CDATA[toUser]]></ToUserName> <FromUserName><![CDATA[fromUser]]></FromUserName> <CreateTime>1348831865</CreateTime> <MsgType><![CDATA[text]]></MsgType> <Content><![CDATA[this is a test]]></Content> <MsgId>9876543210123456</MsgId> </xml> '

def main():
	# root = ElementTree.fromstring(msg)
	# for node in root:
	# 	print node.tag, node.text
	# print root.find('MsgType').text
	root = Element('Articles')
	for i in range(2):
		item = SubElement(root, 'item')

		title = SubElement(item, 'Title')
		title.text = str(i)
		description = SubElement(item, 'Description')
		description.text = str(i) + ' ' + 'test description'
		picUrl = SubElement(item, 'PicUrl')
		picUrl.text = str(i) + ' ' + 'test picurl'
		url = SubElement(item, 'Url')
		url.text = str(i) + ' ' + 'test url'
	tree = ElementTree(root)
	print etree.tostring(root)

def doGet(url, params):
	'''
	Make a HTTP GET request.
	'''
	params = urllib.urlencode(params)
	req = urllib2.Request(url='%s?%s' % (url, params))
	result = urllib2.urlopen(req).read()
	return result


if __name__ == '__main__':
	# main()
	params = {
		'grant_type' : 'client_credential',
		'appid' : 'ca2c526a88744b5e98c0ac548de22725',
		'secret' : '0b331b59196141caa5dcb00df2f73fa9'
	}
	# https://api.yixin.im/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET 
	result = doGet('https://api.yixin.im/cgi-bin/token', params)
	result = simplejson.loads(result)
	print result
	print result['access_token']
