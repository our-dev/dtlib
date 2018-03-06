# coding:utf-8
import os
import random
import string

import requests
# from hashlib import md5
import hashlib
import binascii

__author__ = 'zheng'


def list_have_none_mem(*args):
    """
    检查列表中是否存在None元素,只要有一个为空就返回False
    :return:
    """

    for item in args:
        if item is None:
            return True

    return False


def is_empty(obj):
    """
    检查对象是否为空:
    为null,或者长度为0的字符串
    :param obj:
    :return:
    """

    if obj is None or len(obj) == 0:
        return True
    else:
        return False


#
# def md5value(values):
#     """
#     返回md5后的32位的串
#     :param values:
#     :return:
#     """
#     m = md5()
#     m.update(values)
#     return m.hexdigest()

def md5value(values):
    """
    python3 md5
    :param values:
    :return:
    """
    # 参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
    m = hashlib.md5(values.encode(encoding='utf-8'))
    return m.hexdigest()


def get_rand_salt():
    """
    生成随机salt整数
    :return:
    """
    return random.randint(1, 100)


def md5with_salt(values, salt):
    """
    md5随机数
    :param values:
    :type values:str
    :param salt:
    :type salt:int
    :return:
    """
    res = hashlib.md5(values + str(salt)).hexdigest()
    return res


def hashlibmd5with_salt(values, salt):
    """
    md5随机数
    :param values:
    :type values:str
    :param salt:
    :type salt:int
    :return:
    """
    string = values + str(salt)
    res = hashlib.md5(string.encode(encoding='utf-8')).hexdigest()
    return res


def random_str(length=32):
    """
    生成随机的字符串
    :param length:
    :return:
    """
    str_list = list(string.ascii_letters)
    random.shuffle(str_list)
    return ''.join(str_list[:length])


def create_token():
    """
    创建一个唯一的32位的token

    参考：

    .. code::

        http://blog.useasp.net/archive/2015/11/08/performance-compare-of-python-unique-token-generation-algorithms.aspx
    :return:
    """
    return binascii.b2a_base64(os.urandom(24))[:-1]


def convert_cls_name_to_low(cls_name):
    """
    驼峰式的命名转成中横线的路由格式
    :param cls_name:
    :return:
    """
    str_list = list(cls_name)
    new_str = ''
    for item in str_list:
        char_ord = ord(item)
        if char_ord > 64 and char_ord < 91:
            char_ord = char_ord + 32
            new_str += '-' + chr(char_ord)
        else:
            new_str += item

    if new_str[0] == '-':
        new_str = new_str[1:]

    return new_str


def convert_cls_name_to_low_underline(cls_name):
    """
    驼峰式的命名转成下横线的命名方式
    :param cls_name:
    :return:
    """
    str_list = list(cls_name)
    new_str = ''
    for item in str_list:
        char_ord = ord(item)
        if char_ord > 64 and char_ord < 91:
            char_ord = char_ord + 32
            new_str += '_' + chr(char_ord)
        else:
            new_str += item

    if new_str[0] == '_':
        new_str = new_str[1:]

    return new_str


if __name__ == "__main__":
    # list = [1, 2, None]
    # print(list_have_none_mem(*list))

    # cls_name = 'ApiGtTest'
    # print(convert_cls_name_to_low(cls_name))
    # print(convert_cls_name_to_low_underline(cls_name))

    print(hashlibmd5with_salt('asdf1234', 56))
