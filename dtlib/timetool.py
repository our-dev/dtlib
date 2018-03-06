# coding:utf-8
import time
import datetime
import unittest

from dtlib.dtlog import dlog

__author__ = 'zheng'

default_time_str_fmt = '%Y-%m-%d %H:%M:%S'
ver_tag = '%Y.%m.%d.%H.%M.%S'


# 默认的时间串格式

def get_current_time_string():
    """
    获取年月日 ，时分秒格式字符串
    :return:
    """
    return datetime.datetime.now().strftime(default_time_str_fmt)
    # return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_time_tag():
    """
    返回一个自动生成的版本号的信息
    :return:
    """
    return datetime.datetime.now().strftime(ver_tag)


def get_current_utc_time_string():
    utc_time = get_current_utc_time()

    return utc_time.strftime(default_time_str_fmt)


def get_time_zone():
    """
    获取系统时区, gmt-current_utc,中国是 -8.0
    :return: 
    """
    timezone = time.timezone / 3600
    return timezone


def get_midnight_datetime():
    """
    获取半夜的时间
    :return: 
    """
    now = time.time()
    midnight = now - (now % 86400) + time.timezone
    mid_datetime = datetime.datetime.fromtimestamp(midnight)
    return mid_datetime


def get_utc_midnight_datetime():
    """
    获取当前utc的半夜时间，因为
    1. mongodb中都是没有时区信息，按照utf0来存储
    2. python获取本地时间,带时区信息
    3. python和mongodb做时间
    ？：插数据时，mongodb会去掉python的时区信息，直接当成utc时间。读数据时，python读出的也是utc0时区。
    ？：做数据查询的时候，则带有utc8的时区信息，所以和数据库中的数据做对比时，提前了8个时区
    解决方案：全部用UTC0的时间做查询
    :return: 
    """
    now = time.time()
    midnight = now - (now % 86400)
    mid_datetime = datetime.datetime.fromtimestamp(midnight)
    return mid_datetime


def get_current_time():
    """
    获取前时区的时间
    :return: 
    """
    return datetime.datetime.now()


def get_current_utc_time():
    """
    获取当前的utc0时间
    :return:
    """
    return datetime.datetime.utcnow()


def covert_default_time_str(dt_time):
    """
    时间转成默认的字符格式
    :param dt_time:
    :type datetime.datetime
    :return:
    """
    return dt_time.strftime(default_time_str_fmt)


def convert_default_str_to_dt_time(default_time_str):
    """
    将默认的字符时间转化为datetime时间对象
    :param default_time_str:
    :return:转化后的时间
    :rtype:datetime.datetime
    """
    if default_time_str is not None:
        dt_time = datetime.datetime.strptime(default_time_str, default_time_str_fmt)
        return dt_time
    else:
        return None


class MyTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_current_time_string(self):
        print('current_time:"', get_current_time_string())
        print('current_utc_time:"', get_current_utc_time_string())
        print('machine timezone:', get_time_zone())
        # print(get_current_time_string())
        # print datetime.datetime.utcnow()#UTC0的时间
        # print datetime.datetime.now()
        # print datetime.datetime.astimezone(8)
        # print datetime.tzinfo
        print('current_midnight_time:', get_midnight_datetime().strftime(default_time_str_fmt))
        print('get_utc_midnight_datetime:', get_utc_midnight_datetime().strftime(default_time_str_fmt))

    def test_get_time_tag(self):
        dlog.debug(get_time_tag())


if __name__ == '__main__':
    pass
