"""
表示状态值的类
"""


class ResCode(object):
    """
    HTTP返回值状态码
    """
    ok = 200  # 请求成功
    c_error = 400  # 客户端请求错误
    unauthorized = 401  # 被请求页面需要用户名和密码
    forbidden = 403  # 没有权限被禁止
    s_error = 500  # 服务端出现错误


class UserStatus(object):
    """
    用户状态,用户注册后的状态值表示
    """

    init = 0  # 初始状态
    user_id_changed = 1  # 修改进一次用户ID


class UserRegWay(object):
    """
    用户的注册方式

    """
    web = 0  # 直接通过web来注册的
    wechat_qrcode = 1  # 微信扫码
    mp_app = 2  # 公众平台小程序
