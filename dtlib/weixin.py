# coding:utf-8

from dtlib.wechat.message import LocationMsg, TextMsg
from dtlib.wechat.tplmessage import FormFeedbackTplMsg

__author__ = 'zheng'


def get_msg_type(xml_str):
    """ todo:获取消息类型
    :return:
    """
    return 'text'


class WeChatRobot(object):
    """
    微信机器人
    """

    def __init__(self):
        self.appid = ''
        self.secret = ''
        self.access_token = ''



def decode_wx_text_msg(data):
    """将文本消息转化为字典-waste

    :param data:
    :type return TextMsg
    """
    wx_msg = TextMsg()
    wx_msg.to_user_name = data.find('ToUserName').text
    wx_msg.from_user_name = data.find('FromUserName').text
    wx_msg.create_time = data.find('CreateTime').text
    wx_msg.msg_type = data.find('MsgType').text
    wx_msg.content = data.find('Content').text
    wx_msg.msg_id = data.find('MsgId').text

    return wx_msg


def decode_wx_location_msg(data):
    """
    解析位置信息-waste
    @param data:
    @return:
    """
    wx_msg = LocationMsg()
    wx_msg.to_user_name = data.find('ToUserName').text
    wx_msg.from_user_name = data.find('FromUserName').text
    wx_msg.create_time = data.find('CreateTime').text
    wx_msg.msg_type = data.find('MsgType').text
    wx_msg.location_x = data.find('Location_X').text
    wx_msg.location_y = data.find('Location_Y').text
    wx_msg.scale = data.find('Scale').text
    wx_msg.label = data.find('Label').text
    wx_msg.msg_id = data.find('MsgId').text

    return wx_msg



# 建立函数字典
dict_wx_msg_decode = {
    'text': decode_wx_text_msg,
    'location': decode_wx_location_msg,
}

if __name__ == '__main__':
    feed = FormFeedbackTplMsg()
    print(dir(feed))
