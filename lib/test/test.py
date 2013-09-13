from xml.etree import ElementTree as etree
from xml.etree.ElementTree import Element, SubElement, ElementTree

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


if __name__ == '__main__':
	main()