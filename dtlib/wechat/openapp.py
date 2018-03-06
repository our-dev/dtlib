# coding:utf-8

"""
开放平台应用程序
"""
import json
import requests

from dtlib.wechat.base import WeChatUser
from dtlib.dtlog import dlog

__author__ = 'zheng'


class WeChatOpenApp(object):
    """
    微信应用APP-开放平台网页应用
    """

    def __init__(self):
        self.appid = ''
        self.secret = ''
        self.login_scope = ''

        self.access_token = ''
        self.access_token_time = 0  # 获取token时间，因为有2小时的时效
        self.access_token_expire_in = 0  # 有效时间
        self.refresh_token = ''
        self.refresh_token_time = 0  # 获取token时间，因为有

        # self.auth_access_token = ''  # 用于身份认证的token-只对单个用户用用，不属于此类的内容
        # self.auth_access_token_time = 0
        # self.auth_access_token_expire_in = 0  # 有效时间

    def get_auth_access_token(self, **kwargs):
        """获取auth专用token（不同于基础调用的token,此处）：
        - 服务号回调回调
        - 微信app浏览器网页应用
        - 手机app授权

        三者都是一样的,这个如果有返回值，表明auth是成功的

        通过code去获取网页授权的access_token，可信终端之间的通讯,而且token必须没失效（能够获取用户信息，才证明是登录状态）
        
        返回值：
        
        { 
            "access_token":"ACCESS_TOKEN", 
            "expires_in":7200, 
            "refresh_token":"REFRESH_TOKEN",
            "openid":"OPENID", 
            "scope":"SCOPE",
            "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
        }
        
        
        :param kwargs
        - code: 身份验证票据
        :return:
        """

        wx_code = kwargs.get('code', '')  # 只能用一次，有效时间为5min
        # wx_state = kwargs.get('state', '')  # 在调用微信的时候，传过去的值，非必需

        wx_access_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        wx_access_param = dict(
            appid=self.appid,
            secret=self.secret,
            code=wx_code,
            grant_type='authorization_code'
        )

        res = requests.get(wx_access_url, params=wx_access_param)
        res.encoding = 'utf-8'
        res_json = json.loads(res.text)
        # self.auth_access_token = res_json.get('access_token', '')
        # self.auth_access_token_time = time.time()

        # dlog.debug(res_json)
        return res_json

    def get_auth_user_info(self, **kwargs):
        """
        根据认证token来获取用户详细信息,
        因為目前不清楚，access_token的权限是仅限于当前用户，还是当前的app，
        所以暂先假设是公对本授权用户有访问权限吧。
        
        .. code::
        
            { 
                "openid":"OPENID",
                "nickname":"NICKNAME",
                "sex":1,
                "province":"PROVINCE",
                "city":"CITY",
                "country":"COUNTRY",
                "headimgurl": "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
                "privilege":[
                "PRIVILEGE1", 
                "PRIVILEGE2"
                ],
                "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
            
            }
        
        
        
        """
        auth_access_token_res = kwargs.get('auth_access_token_res', None)
        if auth_access_token_res is None:
            dlog.debug('auth_access_token_res is None')
            return None

        dlog.debug(auth_access_token_res)
        auth_access_token = auth_access_token_res.get('access_token', None)
        if auth_access_token is None:
            return None
        # refresh_token = res_json['refresh_token']
        openid = auth_access_token_res['openid']
        # unionid = auth_access_token_res['unionid']

        wx_user_info_api = 'https://api.weixin.qq.com/sns/userinfo'
        user_info_param = dict(
            access_token=auth_access_token,
            openid=openid,
            lang='zh_CN'
        )
        res_info = requests.get(wx_user_info_api, params=user_info_param)
        res_info.encoding = "utf-8"  # 不然就是乱码
        res_info_dict = json.loads(res_info.text)

        return res_info_dict


class WeChatWebApp(WeChatOpenApp):
    """
    开放平台下的：网站应用
    """

    def __init__(self):
        super(WeChatWebApp, self).__init__()
        self.qr_auth_cb_url = ''  # Web端QR码回调链接


class WeChatMobileApp(WeChatOpenApp):
    """
    开放平台下的：移动应用
    """

    def __init__(self):
        super(WeChatMobileApp, self).__init__()
        # self.qr_auth_cb_url = ''  # app端的不需要
