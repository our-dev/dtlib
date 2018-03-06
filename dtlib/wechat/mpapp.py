# coding:utf-8

"""
MP公众号开发
"""
import json
import time
import urllib

import requests

from dtlib.wechat.openapp import WeChatOpenApp
from dtlib.dtlog import dlog
from dtlib.wechat.decos import mp_token_required

__author__ = 'zheng'


class WeChatMpApp(WeChatOpenApp):
    """
    公众号的APP
    """

    def __init__(self):
        super(WeChatMpApp, self).__init__()
        self.origin_id = ''  # 原始id，一个流水号
        self.wechat_id = ''  # 微信号
        # self.appid = ''
        # self.secret = ''
        self.api_token = ''  # 响应式应答消息的token
        self.encoding_aes_key = ''
        self.webapp_auth_scope = ''  # 'snsapi_base'#'snsapi_userinfo'
        self.mp_auth_cb_url = ''  # 公众号应用的回调
        # 普通接口调用的token--全局共享
        # self.access_token = ''
        # self.access_token_time = 0  # 获取token时间戳，因为有2小时的时效
        # self.token_expires_in = 0  # 到期时间：s

        self.jsapi_timestamp = 0  # 生成签名的时间戳
        self.jsapi_noncestr = 'Wm3WZYTPz0wzccnW'  # 生成签名的随机串
        self.jsapi_signature = '',  # 签名，见附录1

        self.jsapi_ticket = ''
        self.jsapi_ticket_time = 0
        self.jsapi_ticket_expires_in = 0  # 过期时间

    def get_access_token(self):
        """
        获取基础access_token
        """
        token_params = dict(
            grant_type='client_credential',
            appid=self.appid,
            secret=self.secret
        )
        token_url = 'https://api.weixin.qq.com/cgi-bin/token'
        token_res = requests.get(
            token_url,
            params=token_params,
            # verify=False
        )
        token_json = json.loads(token_res.text)
        self.access_token = token_json.get('access_token', '')
        self.access_token_time = time.time()  # 当前时间戳
        self.token_expires_in = int(token_json.get('expires_in', 0))

    @mp_token_required
    def get_callback_ip(self):
        """
        获取微信服务器IP
        :return:
        """

        url = 'https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s' \
              % self.access_token
        res = requests.get(url)

        ip_list = res.text
        return ip_list

    @mp_token_required
    def get_jsapi_ticket(self):
        """
        GET方式请求获得jsapi_ticket（有效期7200秒，开发者必须在自己的服务全局缓存jsapi_ticket）
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' \
              % self.access_token

        res = requests.get(url)
        dlog.debug(res.text)
        res_json = json.loads(res.text)
        if res_json.get('errmsg', None) == 'ok':
            self.jsapi_ticket = str(res_json.get('ticket'))  # unicode转str
            self.jsapi_timestamp = time.time()
            self.jsapi_ticket_expires_in = int(res_json.get('expires_in'))

    def get_auth_callback_url(self, **kwargs):
        """
        生成验证的回调链接
        :param kwargs:redirect_url,state
        :return:
        """
        redirect_url = kwargs.get('redirect_url', '')
        state = kwargs.get('state', '')

        wx_webapp_auth_url = 'https://open.weixin.qq.com/connect/oauth2/authorize' \
                             '?appid=%s' \
                             '&redirect_uri=%s' \
                             '&response_type=%s' \
                             '&scope=%s' \
                             '&state=%s' \
                             '#wechat_redirect' \
                             % (
                                 self.appid,
                                 urllib.quote(redirect_url),
                                 'code',
                                 self.webapp_auth_scope,
                                 state
                             )
        return wx_webapp_auth_url

    # def get_auth_access_token(self, **kwargs):
    #     """
    #     通过code去获取网页授权的access_token（不同于基础调用的token），可信终端之间的通讯,而且token必须有用（能够获取用户信息，才证明是登录状态）
    #     :return:
    #     """
    #
    #     wx_code = kwargs.get('code', '')  # 只能用一次，有效时间为5min
    #
    #     wx_access_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    #     wx_access_param = dict(
    #         appid=self.appid,
    #         secret=self.secret,
    #         code=wx_code,
    #         grant_type='authorization_code'
    #     )
    #
    #     res = requests.get(wx_access_url, params=wx_access_param)
    #     res.encoding = 'utf-8'
    #     res_json = json.loads(res.text)
    #     self.auth_access_token = res_json.get('access_token', '')
    #     self.auth_access_token_time = time.time()
    #
    #     # dlog.debug(res_json)
    #     return res_json
    #
    # def get_auth_use_info(self, **kwargs):
    #     """
    #     获取用户详细信息
    #     :return:
    #     """
    #     openid = kwargs.get('openid', '')
    #     lang = kwargs.get('lang', 'zh_CN')
    #
    #     wx_user_info_api = 'https://api.weixin.qq.com/sns/userinfo'
    #     user_info_param = dict(
    #         access_token=self.auth_access_token,
    #         openid=openid,
    #         lang=lang
    #     )
    #     res_info = requests.get(wx_user_info_api, params=user_info_param)
    #     res_info.encoding = "utf-8"  # 不然就是乱码
    #
    #     dlog.debug(res_info)
    #     return res_info

    @mp_token_required
    def send_tpl_msg(self, post_msg):
        """
        发送模板消息
        """
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % self.access_token
        res = requests.post(url, data=post_msg.encode('utf-8'))
        # res.encoding = 'utf-8'
        dlog.debug(res.text)  # todo 后面来个判断返回值

    @mp_token_required
    def create_menu(self, post_menu_data):
        """
        创建自定义菜单
        :return:
        """
        menu_url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % self.access_token
        menu_res = requests.post(menu_url, data=post_menu_data)
        dlog.debug(menu_res.text)

    @mp_token_required
    def create_temp_qrcode(self):
        """
        创建临时二维码
        :return:
        """

        url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' \
              % self.access_token

        scene_id = '123'

        post_data = """{
            "expire_seconds": 604800,
            "action_name": "QR_SCENE",
            "action_info": {"scene":
                {
                    "scene_id": %s
                }
            }
        }""" % (scene_id)

        res = requests.post(url, data=post_data)
        dlog.debug(res.text)
        # res_dict = json.loads(res.text)
        # ticket = str(res_dict.get('ticket', ''))
        # params_data = dict(
        #     ticket=ticket
        # )
        # get_qrcode_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode'
        #
        # r = requests.get(get_qrcode_url, stream=True,params=params_data)
        # if r.status_code == 200:
        #     with open('qrcode.png', 'wb') as f:
        #         r.raw.decode_content = True
        #         shutil.copyfileobj(r.raw, f)
