# coding:utf-8

"""
常量定义区
"""
__author__ = 'zheng'


class WxConst(object):
    """
    微信开发的常量
    """

    # 发送模板消息
    template_msg_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'  # %ACCESS_TOKEN



# 微信的几种消息类型
wx_msg_type = ['text',
               'event',
               'image',
               'voice',
               'video',
               'location',
               'link',
               'transfer_customer_service'  # 多客服系统
               ]