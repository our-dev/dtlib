"""
一些公用类
"""
from dtlib.tornado.status_cls import ResCode


class ConstData(object):
    """全局配置常量:

    - 通用表单值
    - 返回值

    """

    appid_form = 'appid'
    appkey_form = 'appkey'
    user_form = 'user'
    passwd_form = 'password'

    user_agent_key = 'user_agent'

    res_tpl = '{"code":%s,"msg":"%s","data":%s}'  # 返回消息的模板

    msg_succeed = '{"code":%s,"msg":"success","data":""}' % ResCode.ok  # 操作成功
    msg_fail = '{"code":%s,"msg":"fail","data":""}' % ResCode.s_error  # 操作失败
    msg_unauthorized = '{"code":%s,"msg":"unauthorized","data":""}' % ResCode.unauthorized  # 没有登录认证
    msg_forbidden = '{"code":%s,"msg":"forbidden","data":""}' % ResCode.forbidden  # 操作禁止,没有相应权限
    msg_anonymous = '{"code":%s,"msg":"anoymous user,forbidden","data":""}' % ResCode.forbidden
    msg_args_wrong = '{"code":%s,"msg":"argswrong","data":""}' % ResCode.c_error  # 传入参数错误
    msg_assert_exception = '{"code":%s,"msg":"assert exception","data":""}' % ResCode.s_error  # 进行一次校验,出现异常数据
    msg_none = '{"code":%s,"msg":"not exist","data":""}' % ResCode.s_error  # 空的返回
    msg_exist = '{"code":%s,"msg":"exist","data":""}' % ResCode.s_error  # 已经存在


class QrAuthStatusCode(object):
    """
    自己开发的二维码认证的状态码
    """
    args_wrong = 400  # 服务器未能理解请求，客户端参数错误
    wait = 404  # app扫码后到点击确认前的状态
    cancel = 403  # app端取消授权
    confirm = 200  # app确认可以登录

    # waste = 502  # token已经失效

    none = 500  # 服务器没有找到相应的值，二维码已经失效了
    timeout = 408  # 长连接超过指定周期还没有结果，就超时
