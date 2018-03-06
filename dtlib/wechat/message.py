# coding:utf-8

"""
所有的消息的类型的定义
"""
from xml.etree import ElementTree

__author__ = 'zheng'


class BaseWxMsg(object):
    """基本通用的模板
    """

    def __init__(self, **kwargs):
        raw_msg = kwargs.get('raw_msg', None)
        if raw_msg is None:
            self.to_user_name = ''
            self.from_user_name = ''
            self.create_time = ''
            self.msg_type = ''
            self.raw = ''
            self.msg_xml = ''
            return

        msg_xml = ElementTree.fromstring(raw_msg)
        # self.to_user_name = msg_xml.find('ToUserName', '').text
        self.to_user_name = msg_xml.find('ToUserName').text
        self.from_user_name = msg_xml.find('FromUserName').text
        self.create_time = msg_xml.find('CreateTime').text
        self.msg_type = msg_xml.find('MsgType').text
        self.raw = raw_msg  # 纯文本，原始信息文件
        self.msg_xml = msg_xml  # 解析成xml后的消息对象

        # def __init__(self, raw_msg):
        #     self.to_user_name = raw_msg.find('ToUserName').text
        #     self.from_user_name = raw_msg.find('FromUserName').text
        #     self.create_time = raw_msg.find('CreateTime').text
        #     self.msg_type = raw_msg.find('MsgType').text
        #     self.raw = ''  # 纯文本，原始文本
        # self.msg_id = ''#后面好像没有了2015-11-15


class TransferCustomertMsg(BaseWxMsg):
    """客服消息转换回复
    """

    def __init__(self, **kwargs):
        super(TextMsg, self).__init__(**kwargs)
        raw_msg = kwargs.get('raw_msg', None)
        if raw_msg is None:
            return
        self.msg_type = 'transfer_customer_service'


class TextMsg(BaseWxMsg):
    """微信的文本文件
    """

    def __init__(self, **kwargs):
        super(TextMsg, self).__init__(**kwargs)
        raw_msg = kwargs.get('raw_msg', None)
        if raw_msg is None:
            return
        self.content = self.msg_xml.find('Content').text

    def get_xml_msg(self):
        """
        拼接成标准的通讯文本格式
        :return:
        """
        text_tpl = """
        <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[%s]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        </xml>
        """

        text_xml = text_tpl \
                   % (
                       self.to_user_name,
                       self.from_user_name,
                       self.create_time,
                       self.msg_type,
                       self.content
                   )

        return text_xml


class EventMsg(BaseWxMsg):
    """事件消息,关注和取消关注事件
    """

    def __init__(self, **kwargs):
        super(EventMsg, self).__init__(**kwargs)
        raw_msg = kwargs.get('raw_msg', None)
        if raw_msg is None:
            return
        self.event = self.msg_xml.find('Event').text


class ContextMenuMsg(EventMsg):
    """点击菜单
    """

    def __init__(self, **kwargs):
        super(ContextMenuMsg, self).__init__(**kwargs)
        raw_msg = kwargs.get('raw_msg', None)
        if raw_msg is None:
            return
        self.event_key = self.msg_xml.find('EventKey').text


class QrScanEventMsg(ContextMenuMsg):
    """二维码扫描事件
    """

    def __init__(self, **kwargs):
        super(QrScanEventMsg, self).__init__(**kwargs)
        raw_msg = kwargs.get('raw_msg', None)
        if raw_msg is None:
            return
        self.ticket = self.msg_xml.find('Ticket').text


class LocationMsg(EventMsg):
    """微信的地理信息
    """

    def __init__(self, **kwargs):
        super(LocationMsg, self).__init__(**kwargs)
        raw_msg = kwargs.get('raw_msg', None)
        if raw_msg is None:
            return
        # todo 解析
        self.latitude = ''
        self.longitude = ''
        self.precision = ''

    def get_xml_msg(self):
        """
        拼接成标准的通讯文本格式
        :return:
        """

        location_tpl = """
        <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[LOCATION]]></Event>
        <Latitude>%s</Latitude>
        <Longitude>%s</Longitude>
        <Precision>%s</Precision>
        </xml>
        """

        text_xml = location_tpl \
                   % (
                       self.to_user_name,
                       self.from_user_name,
                       self.create_time,
                       self.event,
                       self.latitude,
                       self.longitude,
                       self.precision
                   )

        return text_xml


class TemplateSendJobFinishMsg(EventMsg):
    """
    公众号发送模板消息之后提醒消息
    """
    event_type = 'TEMPLATESENDJOBFINISH'
    # 状态提示
    success = 'success'
    user_block = 'failed:user block'
    other_status = 'failed: system failed'

    def __init__(self, **kwargs):
        super(TemplateSendJobFinishMsg, self).__init__(**kwargs)
        raw_msg = kwargs.get('raw_msg', None)
        if raw_msg is None:
            return
        self.msg_id = self.msg_xml.find('MsgID').text
        self.status = self.msg_xml.find('Status').text
