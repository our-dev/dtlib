"""
web开发的一些小工具
"""
import datetime
import platform
import unittest

import os
import tornado
from dtlib import timetool
from tabulate import tabulate
from tornado import process

import dtlib
from aiomotorengine import Q

from dtlib.timetool import get_midnight_datetime
from dtlib.tornado.docs import OrgApiCallCounts, ApiCallCounts, OrgAppCallCounts
from dtlib.utils import is_empty


async def save_api_counts(self):
    """
    对全网的接口的调用进行统计，没有时间窗口，只做资源累计
    todo:这个其实可以做成异步，非实时的。
    :param self:
    :type self:BaseHandler
    :return:
    """
    url = self.request.uri
    api = url.split('?')[0]
    api_call_counts = await ApiCallCounts.objects.get(api_name=api)
    if api_call_counts is None:
        api_call_counts = ApiCallCounts(
            api_name=api,
            counts=1,
        )
        api_call_counts.set_default_rc_tag()
        # 暂时先不针对具体的组织统计接口调用信息，或者后续用storm来专门做统计
        await api_call_counts.save()
    else:
        api_call_counts.counts += 1
        await api_call_counts.save()


async def save_app_api_counts(self):
    """
    自动化应用接口的调用统计
    :param self:
    :type self:BaseHandler
    :return:
    """
    url = self.request.uri
    api = url.split('?')[0]

    # 1天的时间差异
    stime = get_midnight_datetime()
    etime = stime + datetime.timedelta(days=1)

    app = await self.get_app()
    org = await self.get_organization()

    app_call_counts_list = await OrgAppCallCounts.objects.filter(
        api_name=api,
        app=app,
        organization=org,
    ).filter(
        Q(rc_time__gte=stime)
        & Q(rc_time__lte=etime)
    ).find_all()

    if is_empty(app_call_counts_list):
        # 如果不存在，则创建一条
        app_call_counts = OrgAppCallCounts(
            api_name=api,
            counts=1,
            app=app,
        )
        await app_call_counts.set_org_tag(http_req=self)
        app_call_counts.set_default_rc_tag()
        await app_call_counts.save()
        return app_call_counts

    assert len(app_call_counts_list) == 1, '接口统计信息数据异常，数据业务唯一性有问题'

    app_call_counts = app_call_counts_list[0]
    app_call_counts.counts += 1
    app_call_counts = await app_call_counts.save()
    return app_call_counts


async def save_user_api_counts(self):
    """
    非装饰器，装饰器的公共函数，
    对单个用户的接口调用次数进行统计
    
    
    1. 查询当天时段是否有此数据
    2. 如果没有，创建一条
    3. 如果有，则在此数据要增加一个计数
    
    :param self:
    :type self:BaseHandler
    :return:
    """
    url = self.request.uri
    api = url.split('?')[0]

    # 1天的时间差异
    stime = get_midnight_datetime()
    etime = stime + datetime.timedelta(days=1)

    user = self.get_current_session_user()
    org = await self.get_organization()

    api_call_counts_list = await OrgApiCallCounts.objects.filter(
        api_name=api,
        owner=user,
        organization=org,
    ).filter(
        Q(rc_time__gte=stime)
        & Q(rc_time__lte=etime)
    ).find_all()

    if is_empty(api_call_counts_list):
        # 如果不存在，则创建一条
        api_call_counts = OrgApiCallCounts(
            api_name=api,
            counts=1
        )
        await api_call_counts.set_org_user_tag(http_req=self)
        api_call_counts.set_default_rc_tag()
        await api_call_counts.save()
        return api_call_counts

    assert len(api_call_counts_list) == 1, '接口统计信息数据异常，数据业务唯一性有问题'

    api_call_counts = api_call_counts_list[0]
    api_call_counts.counts += 1
    api_call_counts = await api_call_counts.save()
    return api_call_counts


def output_sys_info():
    """
    输出服务器相关配置信息
    :param kwargs:
    :return:
    """
    tbl_out = tabulate([
        ['sys_time', timetool.get_current_time_string()],
        ['dtlib', dtlib.VERSION],
        ['py_ver', platform.python_version()],
        ['server_ver', tornado.version],
        ['cpu_count', process.cpu_count()],
    ],
        tablefmt='grid')

    print(tbl_out)

    # 启动前输出系统信息,在日志中有所体现---Ubuntu系统
    os.system('uname -a')
    os.system('ifconfig|grep addr')


def set_default_rc_tag(dictionary):
    """
    设置默认的数据记录标记，utc0时区
    """
    now_time = datetime.datetime.utcnow()  # 只要是涉及到mongodb中的时间储存全部都用utc时间
    dictionary['rc_time'] = now_time
    dictionary['is_del'] = False
    dictionary['del_time'] = None
    return dictionary


class MyTest(unittest.TestCase):
    def test_output_sys_info(self):
        output_sys_info()

    pass
