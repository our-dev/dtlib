"""
环境检测
"""

import socket


def get_host_net_info():
    """
    # 获取本机电脑名
    # 获取本机ip
    :return:
    """
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myname, myaddr


if __name__ == '__main__':
    myname, myaddr = get_host_net_info()
    print(myname)
    print(myaddr)
