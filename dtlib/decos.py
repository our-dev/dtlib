# coding:utf-8
"""
一些装饰器
"""
import functools

import time

from dtlib.dtlog import dlog


def get_time_consuming(method):
    """
    获取运行耗时
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        method(*args, **kwargs)

        end_time = time.time()

        dlog.debug('run time consuming:%s(s)' % (end_time - start_time))

    return wrapper


def aio_get_time_consuming(method):
    """
    获取运行耗时,异步的,py3.5
    :param method:
    :return:
    """

    @functools.wraps(method)
    async def wrapper(*args, **kwargs):
        start_time = time.time()

        await method(*args, **kwargs)

        end_time = time.time()

        dlog.debug('run time consuming:%s(s)' % (end_time - start_time))

    return wrapper