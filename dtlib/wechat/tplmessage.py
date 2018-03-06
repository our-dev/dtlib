# coding:utf-8

"""
主动推送的模板消息文件
"""
from dtlib.wechat.decos import validate_str

__author__ = 'zheng'


class BaseTplMsg(object):
    """
    模板消息基本属性
    """

    def __init__(self):
        self.tpl_id = ''  # 模板ID
        self.url = ''  # 指向的链接
        self.to_user = ''  # 消息送达方


class WarnTplMsg(BaseTplMsg):
    """
    报警模板消息--这个不应该放在标准库里面，
    因为不同的app对应的这个tpl_id不一样，此处仅仅只是提供一个标准的参考
    """

    def __init__(self):
        super(WarnTplMsg, self).__init__()
        self.url = ''  # 打开的详细链接
        self.title = ''  # 标题
        self.time = ''  # 发生时间
        self.addr = ''  # 发生地点
        self.content = ''  # 具体内容
        self.remark = ''  # 其它备注

    @validate_str
    def encode_to_tpl(self, to_user_open_id):
        """
        编码成模板格式的串
        :param to_user_open_id:
        :return:
        """

        post_msg = """{
            "touser": "%s",
            "template_id": "%s",
            "url": "%s",
            "topcolor": "#FF0000",
            "data": {
                "first": {
                    "value": "%s",
                    "color": "#173177"
                },
                "keyword1": {
                    "value": "%s",
                    "color": "#173177"
                },
                "keyword2": {
                    "value": "%s",
                    "color": "#173177"
                },
                "keyword3": {
                    "value": "%s",
                    "color": "#173177"
                },
                "remark": {
                    "value": "%s",
                    "color": "#173177"
                }
            }

        }""" % (
            to_user_open_id,
            self.tpl_id,
            self.url,
            self.title,
            self.time,
            self.addr,
            self.content,
            self.remark
        )

        return post_msg


class FormFeedbackTplMsg(BaseTplMsg):
    """
    表单提交反馈模板信息--这个不应该放在标准库里面，
    因为不同的app对应的这个tpl_id不一样，此处仅仅只是提供一个标准的参考
    """

    def __init__(self):
        # FHtS7eIHeziejKdAgdFtJmYjaaKEJ08GoTexbgD0e2A
        super(FormFeedbackTplMsg, self).__init__()
        self.url = 'http://'  # 打开的详细链接
        self.nickname = ''  # 标题
        self.time = ''  # 发生时间
        self.content = ''  # 具体内容
        self.remark = ''  # 其它备注

    @validate_str
    def encode_to_tpl(self, to_user_open_id):
        """
        编码成模板格式的串
        :param to_user_open_id:
        :return:
        """

        post_msg = """{
            "touser": "%s",
            "template_id": "%s",
            "url": "%s",
            "topcolor": "#FF0000",
            "data": {
                "first": {
                    "value": "%s",
                    "color": "#173177"
                },
                "DateTime": {
                    "value": "%s",
                    "color": "#173177"
                },
                "IP": {
                    "value": "%s",
                    "color": "#173177"
                },
                "remark": {
                    "value": "%s",
                    "color": "#173177"
                }
            }

        }""" % (
            to_user_open_id,
            self.tpl_id,
            self.url,
            self.nickname,
            self.time,
            self.content,
            self.remark
        )

        return post_msg
