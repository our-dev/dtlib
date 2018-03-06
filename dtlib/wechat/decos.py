# coding:utf-8

"""
装饰器,use tornado
"""
import functools
import time
import urllib
from dtlib.dtlog import dlog

__author__ = 'zheng'


def validate_str(method):
    """
    保证token一直是有效的,公众平台的，因为没有refresh_token之说，所以说分开写,装饰器
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        检查所有的数据成员是否是str变量 ，不允许 有unicode变量
        """
        for item in dir(self):
            if item[:2] == '__':  # 排除所有的内置对象
                continue
            item_value = getattr(self, item)
            if callable(item_value):  # 排除所有的函数
                continue
            # if isinstance(item_value, unicode):
            #     dlog.exception('[Error]member-name:%s,value:%s' % (item, item_value))
            #     return 'Error encoding characters'

        return method(self, *args, **kwargs)

    return wrapper


def mp_token_required(method):
    """
    保证token一直是有效的,公众平台的，因为没有refresh_token之说，所以说分开写,装饰器
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        :type self WeChatMpApp
        """
        if self.access_token == '' \
                or (time.time() - self.access_token_time) >= self.token_expires_in:
            self.get_access_token()  # 重新获取accesstoken
        return method(self, *args, **kwargs)

    return wrapper



def auth_token_required(method):
    """
    需要auth身份认证的token
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        :type self WeChatMpApp
        """
        if self.auth_access_token == '' \
                or (time.time() - self.auth_access_token_time) >= self.auth_access_token_expire_in:
            self.get_auth_access_token()  # 重新获取accesstoken
        return method(self, *args, **kwargs)

    return wrapper



def mp_jsapi_ticket_required(**kwargss):  # 装饰器参数
    """
    保证jsapi_ticket一直是有效的,公众平台的,装饰器
    :param method:
    :return:
    """

    def _deco(method):  # 函数指针
        def wrapper(self,*args, **kwargs):  # 函数参数
            """
            :type self base.handlers.BaseHandler
            """
            mp_app = kwargss.get('wx_mp_app', None)
            if mp_app.jsapi_ticket == '' \
                or (time.time() - mp_app.jsapi_ticket_time) >= mp_app.jsapi_ticket_expires_in:
                mp_app.get_jsapi_ticket()  # 重新获取jsapi_ticket
            return method(self, *args, **kwargs)

        return wrapper

    return _deco






def wechat_auth_required(**kwargss):  # 装饰器参数
    """
    如果微信用户没有进行授权，则会导入到微信客户端的授权页面，
    如果授权了，则直接进入客户页面(可以做成第三方库)
    :param kwargs:
    :return:
    """

    def _deco(method):  # 函数指针
        def wrapper(self):  # 函数参数
            """
            :type self base.handlers.BaseHandler
            """
            wx_mp_help = kwargss.get('wx_mp_app', None)
            relative_path = kwargss.get('relative_path', '')

            dlog.debug("session_id:%s" % self.session.id)

            next_url = self.request.uri  # 回调之后继续重定向的路径,带参数
            dlog.debug('request.uri:%s', next_url)
            # next_url = '/%s%s' % (relative_path, next_url)  # 加上一个相对路径,因为有nginx做了一次匹配的,此项目只是一个二级路径
            if wx_mp_help is None:
                self.write('No wechat media platform')
                return

            next_para = dict(
                next=next_url
            )

            redirect_url = '%s?%s' % (wx_mp_help.mp_auth_cb_url, urllib.urlencode(next_para))

            if ('login_status' in self.session) and (self.session['login_status'] is True):
                return method(self)

            # 如果不是登录的状态，则进行微信第三方认证
            state = self.session.id

            wx_webapp_auth_url = wx_mp_help.get_auth_callback_url(
                redirect_url=redirect_url, state=state)

            dlog.debug(wx_webapp_auth_url)
            self.redirect(wx_webapp_auth_url)
            return

        return wrapper

    return _deco
