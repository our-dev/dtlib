"""
the config of mongo
"""


class MongodbSetting(object):
    """
    数据库的设置类
    """

    def __init__(self, host='localhost', port=27017, db_name='test', collection='logs',
                 user_name=None, user_pwd=None):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.user_name = user_name
        self.user_pwd = user_pwd
