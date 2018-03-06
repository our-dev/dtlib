"""
mongodb的一些公共操作
"""
import asyncio
import os

import sys

from dtlib.tornado.tools import call_subprocess


async def set_mongo_ttl_index(col_name, index_filed_name, expire_sec):
    """
    设置超时删除的TTL
    :param col_name:集合名称
    :param index_filed_name:字段名称
    :param expire_sec:超时时间
    :type expire_sec:int
    :return:
    """
    index_info = await col_name.index_information()
    print(index_info)
    ttl_index_name = index_filed_name + '_1'
    if ttl_index_name in index_info:
        await col_name.drop_index(ttl_index_name)
        print('remove old TTL index:%s' % ttl_index_name)

    await col_name.ensure_index(index_filed_name, expireAfterSeconds=expire_sec)


def get_mongodb_version():
    """
    获取当前mongodb服务器的版本号
    :parameter db:版本号
    :return: 
    """
    cmd = 'mongod --version'
    line = os.popen(cmd).readlines()
    print(line)
    ver = line[0].split('\n')[0]
    print(ver)

    return ver


def get_pip_list():
    """
    获取所有的依赖包的信息
    :return: 
    """
    cmd = 'pip freeze'

    line = os.popen(cmd).readlines()
    # print(line)

    new_list = []
    for item in line:
        item = item.strip('\n')
        new_list.append(item)

    return new_list


def get_python_version():
    """
    获取python的版本号
    :return: 
    """
    import platform
    return platform.python_version()



if __name__ == '__main__':
    get_pip_list()
    pass
