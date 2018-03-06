# coding:utf-8

"""
一些标准的类
"""


class MyFunReturn(object):
    """
    函数返回的标准类,带数据和
    """

    def __init__(self, **kwargs):
        code = kwargs.get('code', 200)
        msg = kwargs.get('msg', '')
        data = kwargs.get('data', None)

        self.code = code
        self.msg = msg
        self.data = data


my_assert_return = MyFunReturn(code=500, msg='assert exception return')  # 断言异常,返回
my_forbidden_return = MyFunReturn(code=403, msg='forbidden return')  # 权限问题,返回
