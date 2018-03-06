"""
在web开发中都要用到的一些常用字典对
"""


class ValueDict(object):
    """
    数值字典，对于那些一次写入的数据，做一些冗余的写入工作
    """

    def __init__(self, value, key):
        self.key = key
        self.value = value


class BaseDictClass(object):
    """
    所有的dict的基类
    """

    def get_dict(self):
        """
        将所有的名值对转化为dict，作废
        :return:
        """

        res_dict = {}
        mem_list = dict(self)
        for item in mem_list:
            # 除去很私有变量
            if item.startswith('__'):
                continue
            # 除去方法成员
            cls_attr = getattr(self, item)
            if callable(cls_attr):
                continue
            res_dict.update(a=cls_attr.value)

        print(res_dict)

    @classmethod
    def get_value_by_attrib_name(cls, item_name):
        """

        :param item_name:
        :return:
        :rtype:ValueDict
        """

        cls_attr = getattr(cls, item_name)
        return cls_attr


class OperationDict(BaseDictClass):
    """
    一些操作的字典
    """

    login = ValueDict(0, 'login')
    logout = ValueDict(1, 'logout')
    create = ValueDict(2, 'create')
    read = ValueDict(3, 'read')
    update = ValueDict(4, 'update')
    delete = ValueDict(5, 'delete')


class ClientTypeDict(BaseDictClass):
    """
    客户端字典查询
    """
    browser = ValueDict(0, 'browser')  # 浏览器
    mobile = ValueDict(1, 'mobile')  # 移动端
    android = ValueDict(2, 'android')
    ios = ValueDict(3, 'ios')
    api = ValueDict(4, 'api')  # 通过api登录


class UserOrigin(BaseDictClass):
    """
    用户来源
    """
    wechat = ValueDict(0, 'wechat')  # 微信授权

    network = ValueDict(1, 'network')
    invite = ValueDict(2, 'invite')

    alipay = ValueDict(3, 'alipay')
    weibo = ValueDict(4, 'weibo')  # 微博授权

    phone = ValueDict(5, 'phone')
    email = ValueDict(6, 'email')


if __name__ == '__main__':
    # a = OperationDict()
    # a.get_dict()

    a= OperationDict.get_value_by_attrib_name('login')
    print(a)
    pass
