from xml.etree import ElementTree

msg = '<xml> <ToUserName><![CDATA[toUser]]></ToUserName> <FromUserName><![CDATA[fromUser]]></FromUserName> <CreateTime>1348831865</CreateTime> <MsgType><![CDATA[text]]></MsgType> <Content><![CDATA[this is a test]]></Content> <MsgId>9876543210123456</MsgId> </xml> '

def main():
	root = ElementTree.fromstring(msg)
	for node in root:
		print node.tag, node.text
	print root.find('MsgType').text

if __name__ == '__main__':
	main()