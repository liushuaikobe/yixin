MSG_TYPE_NODE_NAME = 'MsgType'

TEXT_TYPE = 'text'
PIC_TYPE = 'image'
LOCATION_TYPE = 'location'
EVENT_TYPE = 'event'

GET_TOKEN_URL = 'https://api.yixin.im/cgi-bin/token'
ADD_MENU_URL = 'https://api.yixin.im/cgi-bin/menu/create?access_token='
DELETE_MENU_URL = 'https://api.yixin.im/cgi-bin/menu/delete'
QUERY_CURRENT_MENU_URL = 'https://api.yixin.im/cgi-bin/menu/get'


REPLY_TEXT_TEMPLATE = '<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[text]]></MsgType> <Content><![CDATA[%s]]></Content> </xml>'
REPLY_MUSIC_TEMPLATE = '<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[music]]></MsgType> <Music> <Title><![CDATA[%s]]></Title> <Description><![CDATA[%s]]></Description> <MusicUrl><![CDATA[%s]]></MusicUrl> <HQMusicUrl><![CDATA[%s]]></HQMusicUrl> </Music> </xml> '
REPLY_NEWS_TEMPLATE = '<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[news]]></MsgType> <ArticleCount>%s</ArticleCount> %s </xml> '