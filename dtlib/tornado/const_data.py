"""
本项目中用到的一些常量
"""


class FieldDict(object):
    """
    字段字典
    """
    key_async_redis_pool = 'async_redis_pool'  # 异步的redis连接池
    key_sync_redis_pool = 'sync_redis_pool'

    key_async_mongo_pool = 'async_mongo_pool'  # 异步Mongo连接池

    # user_status_init = 0  # 初始用户状态,可以修改用户名,密码没有设置
    # user_status_final = 1  # 已经修改完毕用户名

    # enterprise = ValueDict(7, 'enterprise')  # 企业批量导入后回流进来的，后面可以多看看其它的app的做法


class SessionKey(object):
    """
    session的字段
    """
    log_session = 'log_session'

    test_web_app = 'test_web_app'
    """测试web的应用"""
    login_status = 'login_status'
    """登录状态"""


if __name__ == '__main__':
    # adic = {}
    # adic[ClientType.ios] = ClientType.android
    #
    # print(adic)
    # print(json.dumps(ClientType.android))
    pass
