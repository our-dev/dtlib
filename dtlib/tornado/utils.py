"""
web开发的一些小工具 + 
- 账号系统的功能
"""
import math
import datetime
import platform
import unittest
import os
import tornado

from tabulate import tabulate
from tornado import process

from bson import ObjectId
from pymongo import DESCENDING

import dtlib
from dtlib import timetool
from dtlib import jsontool
from dtlib.utils import list_have_none_mem
from dtlib.web.constcls import ConstData
from dtlib.web.tools import get_std_json_response

# from aiomotorengine import Q
# from dtlib.timetool import get_midnight_datetime
# from dtlib.tornado.docs import OrgApiCallCounts, ApiCallCounts, OrgAppCallCounts
# from dtlib.utils import is_empty


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
    db = self.get_async_mongo()
    api_call_col = db.api_call_counts
    api_call_counts = await api_call_col.find_one({'api_name': api})
    if api_call_counts is None:
        new_api_call = dict(
            api_name=api,
            counts=1,
        )
        new_api_call = set_default_rc_tag(new_api_call)
        # 暂时先不针对具体的组织统计接口调用信息，或者后续用storm来专门做统计
        await api_call_col.insert_one(new_api_call)
    else:
        await api_call_col.update_one({'api_name': api}, {'$inc': {'counts': 1}})


#
#
# async def save_app_api_counts(self):
#     """
#     自动化应用接口的调用统计
#     :param self:
#     :type self:BaseHandler
#     :return:
#     """
#     url = self.request.uri
#     api = url.split('?')[0]
#
#     # 1天的时间差异
#     stime = get_midnight_datetime()
#     etime = stime + datetime.timedelta(days=1)
#
#     app = await self.get_app()
#     org = await self.get_organization()
#
#     app_call_counts_list = await OrgAppCallCounts.objects.filter(
#         api_name=api,
#         app=app,
#         organization=org,
#     ).filter(
#         Q(rc_time__gte=stime)
#         & Q(rc_time__lte=etime)
#     ).find_all()
#
#     if is_empty(app_call_counts_list):
#         # 如果不存在，则创建一条
#         app_call_counts = OrgAppCallCounts(
#             api_name=api,
#             counts=1,
#             app=app,
#         )
#         await app_call_counts.set_org_tag(http_req=self)
#         app_call_counts.set_default_rc_tag()
#         await app_call_counts.save()
#         return app_call_counts
#
#     assert len(app_call_counts_list) == 1, '接口统计信息数据异常，数据业务唯一性有问题'
#
#     app_call_counts = app_call_counts_list[0]
#     app_call_counts.counts += 1
#     app_call_counts = await app_call_counts.save()
#     return app_call_counts


# async def save_user_api_counts(self):
#     """
#     非装饰器，装饰器的公共函数，
#     对单个用户的接口调用次数进行统计
#
#
#     1. 查询当天时段是否有此数据
#     2. 如果没有，创建一条
#     3. 如果有，则在此数据要增加一个计数
#
#     :param self:
#     :type self:BaseHandler
#     :return:
#     """
#     url = self.request.uri
#     api = url.split('?')[0]
#
#     # 1天的时间差异
#     stime = get_midnight_datetime()
#     etime = stime + datetime.timedelta(days=1)
#
#     user = self.get_current_session_user()
#     org = await self.get_organization()
#
#     api_call_counts_list = await OrgApiCallCounts.objects.filter(
#         api_name=api,
#         owner=user,
#         organization=org,
#     ).filter(
#         Q(rc_time__gte=stime)
#         & Q(rc_time__lte=etime)
#     ).find_all()
#
#     if is_empty(api_call_counts_list):
#         # 如果不存在，则创建一条
#         api_call_counts = OrgApiCallCounts(
#             api_name=api,
#             counts=1
#         )
#         await api_call_counts.set_org_user_tag(http_req=self)
#         api_call_counts.set_default_rc_tag()
#         await api_call_counts.save()
#         return api_call_counts
#
#     assert len(api_call_counts_list) == 1, '接口统计信息数据异常，数据业务唯一性有问题'
#
#     api_call_counts = api_call_counts_list[0]
#     api_call_counts.counts += 1
#     api_call_counts = await api_call_counts.save()
#     return api_call_counts


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


def wrap_org_tag(origin_dict, org_id):
    """
    包装加上组织信息
    :param org_id:
    :type org_id:str
    :return:
    """
    org_obj_id = ObjectId(str(org_id))
    origin_dict.update(organization=org_obj_id)
    return origin_dict


def wrap_project_tag(origin_dict, project):
    """

    :param origin_dict:
    :param project: Project的aio orm
    :type project:Project
    :return:
    """
    origin_dict.update(pro_id=project['_id'])  # 转化为ObjectId保存
    origin_dict.update(pro_name=project['project_name'])
    return origin_dict


async def get_org_data_paginator(self, *args, **kwargs):
    """
    直接传入项目名称和表的名称,返回分页的信息
    :param self:
    :param args:
    :param kwargs:col_name
    :return:
    """
    page_idx = self.get_argument("page_idx", '1')
    page_cap = self.get_argument('page_cap', '20')  # 一页的记录容量-var
    page_idx = int(page_idx)
    page_size = int(page_cap)  # 一页显示40条数据

    col_name = kwargs.get('col_name', None)
    pro_id = kwargs.get('pro_id', None)
    tag = kwargs.get('tag', [])  # 需要展示的dict
    hide_fields = kwargs.get('hide_fields', None)  # 需要隐藏的字段,一个dict
    """:type:dict"""

    if list_have_none_mem(*[col_name, ]):
        return ConstData.msg_args_wrong

    # col_name = 'unit_test_data'

    mongo_coon = self.get_async_mongo()
    mycol = mongo_coon[col_name]

    user_org = await self.get_organization()
    """:type:Organization"""

    if user_org is None:
        return ConstData.msg_none

    find_condition = {
        "organization": ObjectId(user_org),
        "is_del": False
    }

    # if pro_id is None:
    if pro_id:
        find_condition['pro_id'] = ObjectId(str(pro_id))
        if tag != []:
            if isinstance(tag, list) is False:
                return ConstData.msg_args_wrong
            tag_condition = {
                '$in': tag
            }
            if 'default' in tag:
                # todo: remove the next release
                find_condition['$or'] = [{'tag': tag_condition}, {'tag': {'$exists': False}}]
            else:
                find_condition['tag'] = tag_condition

    msg_details = mycol.find(find_condition, hide_fields).sort([('rc_time', DESCENDING)])  # 升序排列
    msg_details_cnt = await msg_details.count()
    msg_details = msg_details.skip(page_size * (page_idx - 1)).limit(page_size)  # 进行分页

    total_page = math.ceil(msg_details_cnt / page_size)  # 总的页面数
    # dlog.debug('total page:%s' % total_page)
    # dlog.debug('msg_details.count():%s' % msg_details_cnt)

    msg_content_list = await msg_details.to_list(page_size)

    page_res = dict(
        page_idx=page_idx,
        page_total_cnts=total_page,
        page_cap=page_size,
        page_data=msg_content_list
    )

    return get_std_json_response(data=jsontool.dumps(page_res, ensure_ascii=False))


async def get_org_data(self, **kwargs):
    """
    获取本组织私有的数据
    :param self:
    :type self BaseHandler
    :param kwargs:
    :return:
    """
    collection = kwargs.get('collection', None)
    project_id = kwargs.get('pro_id', None)
    org = await self.get_organization()

    if org is None:
        return None

    db = self.get_async_mongo()
    col = db[collection]

    # 用project做筛选
    if project_id is not None:
        project_obj_id = ObjectId(str(project_id))
        data = dict(
            organization=ObjectId(org),
            project=project_obj_id,
            is_del=False
        )
    else:
        # 没有做筛选
        data = dict(
            organization=ObjectId(org),
            is_del=False
        )
    org_data = col.find(data).sort([('rc_time', DESCENDING)])
    org_cnt = await org_data.count()
    return await org_data.to_list(org_cnt)


def user_id_is_legal(user_id):
    """
    id检查

    - 不小于6位
    - 只能是数字,字母，下划线组合

    :param passwd:
    :return:
    """

    if len(user_id) < 6:
        return False

    # todo 还有其它更严格的检查
    return True


class MyTest(unittest.TestCase):
    def test_output_sys_info(self):
        output_sys_info()

    pass
