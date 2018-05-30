import functools
import json
import os
import traceback

# from dtlib.tornado.ttl_docs import AccessToken
from dtlib.tornado.utils import save_api_counts
#, save_user_api_counts, save_app_api_counts
from dtlib.web.constcls import ConstData
from dtlib.web.tools import get_jsonp_res


def allow_cors_post(method):
    """
    允许浏览器跨域post,在应用层动态的设置,放在最外层
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        :type self tornado.web.RequestHandler
        """
        req_origin = self.request.headers.get('Origin', '*')
        self.set_header('Access-Control-Allow-Origin', req_origin)
        return method(self, *args, **kwargs)

    return wrapper


def api_counts(is_async=True):
    """
    针对全网的接口的使用量的统计
    :param is_async:
    :return:
    """

    def _api_counts(method):
        """
        带参数，综合了同步和异步的装饰器，必须带参数
        :param method:
        :return:
        """

        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            """
            :type self MyBaseHandler
            """
            if is_async:
                await method(self, *args, **kwargs)
            else:
                method(self, *args, **kwargs)

            await save_api_counts(self)

        return wrapper

    return _api_counts


def test_token_required(is_async=True, test_token='1234'):
    def _async_token_required(method):
        """
        带参数，综合了同步和异步的装饰器，必须带参数
        :param method:
        :return:
        """

        # @api_counts()
        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            """
            :type self MyBaseHandler
            """
            token = self.get_argument('tt', None)
            if token is None:
                self.write(ConstData.msg_args_wrong)
                return
            if token != test_token:
                self.write(ConstData.msg_forbidden)
                return

            if is_async:
                await method(self, *args, **kwargs)
            else:
                method(self, *args, **kwargs)

        return wrapper

    return _async_token_required


def token_required(is_async=True):
    def _async_token_required(method):
        """
        带参数，综合了同步和异步的装饰器，必须带参数
        :param method:
        :return:
        """

        @api_counts()
        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            """
            :type self MyBaseHandler
            """
            log_session = await self.set_session_by_token(cookie_enable=False)

            if log_session is None:
                self.write(ConstData.msg_unauthorized)
                return

            if is_async:
                await method(self, *args, **kwargs)
            else:
                method(self, *args, **kwargs)
            # await save_user_api_counts(self)

        return wrapper

    return _async_token_required


def app_api_counts(is_async=True):
    """自动化应用的接口的统计"""

    def _api_counts(method):
        """
        带参数，综合了同步和异步的装饰器，必须带参数
        :param method:
        :return:
        """

        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            """
            :type self MyBaseHandler
            """
            if is_async:
                await method(self, *args, **kwargs)
            else:
                method(self, *args, **kwargs)

            # await save_app_api_counts(self)

        return wrapper

    return _api_counts


def app_token_required(is_async=True):
    def _async_token_required(method):
        """
        应用程序的token认证
        :param method:
        :return:
        """

        @app_api_counts()
        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            """
            :type self MyBaseHandler
            """
            log_session = await self.set_session_by_token(cookie_enable=False)

            if log_session is None:
                self.write(ConstData.msg_unauthorized)
                return

            if is_async:
                await method(self, *args, **kwargs)
            else:
                method(self, *args, **kwargs)

        return wrapper

    return _async_token_required


# def async_token_required_json(method):
#     """
#     - 验证使用账号密码的低频API是否经过认证
#     - py3 finished
#     - 不再使用会话,而是token
#     - 此方法是在别人在Post一个json的时候 ，里面包含token字段
#     :param method:
#     :return:
#     """
#
#     @api_counts()
#     @functools.wraps(method)
#     async def wrapper(self, *args, **kwargs):
#         """
#         :type self MyBaseHandler
#         """
#
#         post_byte = self.request.body
#         if len(post_byte) == 0:
#             return None
#         post_str = str(post_byte, encoding="utf-8")
#         json_res = json.loads(post_str)
#
#         token = json_res.get('token', None)
#
#         callback = self.get_argument('callback', None)
#
#         self.set_header('Content-Type', 'application/json')
#         self.set_header('charset', 'utf-8')
#
#         if token is None:
#             self.write(get_jsonp_res(callback, ConstData.msg_unauthorized))
#             return
#
#         self.set_cookie('token', token)
#
#         log_session = await AccessToken.objects.get(token=token)
#         """:type:AccessToken"""
#
#         if log_session is None:
#             self.write(get_jsonp_res(callback, ConstData.msg_unauthorized))
#             return
#
#         # 在此处直接赋值存储session,一些临时变量在此处缓存
#         self.token = token  # 本次请求都会用到token,相当于会话标识
#         self.cache_log_session = log_session
#
#         await method(self, *args, **kwargs)
#
#     return wrapper


def wrap_track_back(method):
    """
    打印出异常信息
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            return

    return wrapper


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    print(os.path.abspath('.'))
