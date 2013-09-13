MSG_TYPE_NODE_NAME = 'MsgType'

TEXT_TYPE = 'text'
PIC_TYPE = 'image'
LOCATION_TYPE = 'location'

REPLY_TEXT_TEMPLATE = '<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[text]]></MsgType> <Content><![CDATA[%s]]></Content> </xml>'
REPLY_MUSIC_TEMPLATE = ' <xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[music]]></MsgType> <Music> <Title><![CDATA[%s]]></Title> <Description><![CDATA[%s]]></Description> <MusicUrl><![CDATA[%s]]></MusicUrl> <HQMusicUrl><![CDATA[%s]]></HQMusicUrl> </Music> </xml> '