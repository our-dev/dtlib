"""
环境检测
"""

import socket
import unittest


def out_put_py_env():
    """
    输出python版本号和操作系统
    :return:
    """
    import sys
    print(sys.version)
    print(sys.platform)


def get_host_net_info():
    """
    # 获取本机电脑名
    # 获取本机ip
    :return:
    """
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myname, myaddr


class MyTest(unittest.TestCase):

    def test_get_host_net_info(self):
        myname, myaddr = get_host_net_info()
        print(myname)
        print(myaddr)

    def test_output_py_env(self):
        out_put_py_env()
