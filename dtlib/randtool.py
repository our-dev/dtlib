# coding:utf-8
"""
生成随机数
"""

import random
import time
import uuid
from hashlib import md5

__author__ = 'zheng'


def generate_rand_id(sstr=None):
    """
    生成一组16进制的随机数,32位
    :param sstr:
    :return:
    """

    ti = int(time.time())
    if not sstr:
        string = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        random.shuffle(string)
        sstr = ''.join(string)
    rand = str(random.randint(0, 99999))
    res = str(ti) + sstr + rand
    res = md5(res.encode('utf-8')).hexdigest()
    return res


def get_uuid1_key():
    """
    获取唯一码,32个的16进制
    :return:
    """
    uuid_str = uuid.uuid1().hex
    return uuid_str


def generate_uuid_token():
    """
    生成一个40位数的16进制的token字段串，
    因为考虑到直接uuid生成存在连续性问题，
    后面再加个8位的随机数
    :return: 
    """
    uuid_str = get_uuid1_key()
    rand_str = generate_rand_id()
    rand_str = rand_str[0:8]
    token = uuid_str + rand_str
    return token


def get_uuid3_key(domain='default.domain.com'):
    """
    根据域来获得唯一的ID,但同一命名空间的同一名字生成相同的uuid
    :param domain:
    :return:
    """
    uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, domain).hex
    return uuid_str


def demo_get_uuid1():
    for _ in range(20):
        print(get_uuid1_key())


if __name__ == '__main__':
    demo_get_uuid1()
    # print(generate_uuid_token())
    # print(generate_uuid_token())
