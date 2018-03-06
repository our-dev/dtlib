# coding:utf-8
"""
微信基本对象
"""
from dtlib.dtlog import dlog

__author__ = 'zheng'


class WeChatUser(object):
    """
    微信账号信息
    """

    def __init__(self):
        self.openid = ''
        self.nickname = ''
        self.sex = ''
        self.province = ''
        self.city = ''
        self.country = ''
        self.headimgurl = ''
        self.privilege = []
        self.unionid = ''

    def init_by_res_dict(self, res_info_json):
        """
        根据微信服务器返回值再初始化本类
        :return: 
        """
        self.city = res_info_json['city']
        self.country = res_info_json['country']
        self.headimgurl = res_info_json['headimgurl']
        self.nickname = res_info_json['nickname']
        self.openid = res_info_json['openid']
        self.privilege = res_info_json['privilege']
        self.province = res_info_json['province']
        self.sex = res_info_json['sex']
        self.unionid = res_info_json['unionid']

    def debug_out(self):
        """
        打印调试输出
        :return:
        """
        user_info = 'nickname:%s,\nsex:%s,\nprovice:%s,\nlogin succeed by wechat' \
                    % (self.nickname, self.sex, self.province)
        dlog.debug(user_info)

    def debug_json_code(self):
        for item in dir(self):
            if item[:2] == '__':  # 排除所有的内置对象
                continue
            item_value = getattr(self, item)
            if callable(item_value):  # 排除所有的函数
                continue

            print("self.%s = res_info_json['%s']" % (item, item))


if __name__ == '__main__':
    ins = WeChatUser()
    ins.debug_json_code()
