#！coding:utf8

"""
network tools
"""
import requests
import re
import socket

__author__ = 'zheng'




def get_wan_ip():
    """
    查看本机公网IP
    :return:
    """
    # ip_res = requests.get("http://www.whereismyip.com")
    # wan_ip = re.search('\d+\.\d+\.\d+\.\d+', ip_res.text).group(0)
    #
    # return wan_ip
    #todo 因为此网站经常访问不到，所以先注销掉
    return '127.0.0.1'


def get_domain_ip(domain_name):
    """
    获取域名的IP地址
    可视化验证修改的域名
    :return:
    """
    ip_addr = socket.gethostbyname(domain_name)
    # glog.debug('api server ip addr:%s' % ip_addr)
    return ip_addr
