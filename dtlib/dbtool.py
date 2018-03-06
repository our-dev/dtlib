"""
数据库相关
"""


class DbSetting(object):
    """
    数据库的设置类
    """

    def __init__(self, **kwargs):
        self.alias = kwargs.get('alias', '')  # 别名
        self.host = kwargs.get('host', '')  # 数据库主机
        self.port = kwargs.get('port', 0)  # 27017
        self.db_name = kwargs.get('db_name', '')  # 数据库名称
        self.user_name = kwargs.get('user_name', '')  # 登录名
        self.user_pwd = kwargs.get('user_pwd', '')  # 登录密码
        self.max_connections = kwargs.get('max_connections', 1)#连接池



class RedisConf(object):
    """
    redis的设置
    """

    def __init__(self, **kwargs):
        self.host = kwargs.get('host', 'localhost')  # 服务器
        self.port = kwargs.get('port', 6379)
        self.db = kwargs.get('db', 0)
        self.max_connections = kwargs.get('max_connections', 1)
        self.password = kwargs.get('password', None)
