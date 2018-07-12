import functools

import math

from dtlib.dtlog import dlog

from dtlib.web.constcls import ConstData
from dtlib.web.tools import get_std_json_response

from dtlib import jsontool


def my_async_jsonp(method):
    """
    异步的jsonp格式包装
    后面推荐使用：deco_jsonp()， 2017-05-31
    :param method:
    :return:
    """

    @functools.wraps(method)  # 加入此句后，可以 生成 文档
    async def wrapper(self, *args, **kwargs):
        """
        异步Jsonp包装
        :param self:
        :type self: BaseHandler
        :param args:
        :param kwargs:
        :return:
        """
        dlog.warn('这个是旧的函数，请尽快使用 deco_jsonp()替代，2017-06-06')

        callback = self.get_argument('callback', None)
        if callback is None:
            res_str = await method(self, *args, **kwargs)
        else:
            res = await method(self, *args, **kwargs)
            res_str = '%s(%s)' % (callback, res)

        if res_str is None:
            res_str = ConstData.msg_none

        self.write(res_str)

    return wrapper


def my_async_paginator(method):
    """
    对某个查询结果进行分页,自带jsonp
    标准的分页器
    :param method:
    :return:
    """

    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        # callback = self.get_argument('callback', None)
        page_idx = self.get_argument('page_idx', '1')  # 页面索引号-var
        page_cap = self.get_argument('page_cap', '15')  # 一页的记录容量-var

        page_idx = int(page_idx)
        page_cap = int(page_cap)

        my_paginator_data = await method(self, *args, **kwargs)

        if my_paginator_data is None:
            rcs_len = 0
            my_paginator_data = []
        else:
            rcs_len = len(my_paginator_data)  # 记录总长度

        # 前端分页显示的内容
        page_total_cnts = int(math.ceil(rcs_len / page_cap))  # 页面的总数

        # 计算分页数据
        start_idx = (page_idx - 1) * page_cap  # 起始记录

        end_idx = start_idx + page_cap
        if end_idx > rcs_len:
            end_idx = rcs_len  # 防止溢出

        page_data = my_paginator_data[start_idx:end_idx]  # 取出分页的数据

        page_data_json_list = []
        for item in page_data:
            page_data_json_list.append(item)

        res_dict = dict(
            page_total_cnts=page_total_cnts,
            page_idx=page_idx,
            page_cap=page_cap,
            page_data=page_data_json_list,
            count=rcs_len
        )

        res_str = jsontool.dumps(res_dict, ensure_ascii=False)
        return res_str

    return wrapper

def my_async_paginator_motor(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):

        page_idx = self.get_argument('page_idx', '1')  # 页面索引号-var
        page_cap = self.get_argument('page_cap', '15')  # 一页的记录容量-var

        page_idx = int(page_idx)
        page_cap = int(page_cap)

        my_paginator_data = await method(self, *args, **kwargs)

        page_count = await my_paginator_data.count()
        msg_details = my_paginator_data.skip(page_cap * (page_idx - 1)).limit(page_cap)  # 进行分页

        total_page = math.ceil(page_count / page_cap)  # 总的页面数

        msg_content_list = await msg_details.to_list(page_cap)

        res_dict = dict(
            page_total_cnts=total_page,
            page_idx=page_idx,
            page_cap=page_cap,
            page_data=msg_content_list,
        )



        res_str = jsontool.dumps(res_dict, ensure_ascii=False)

        return res_str

    return wrapper


def my_async_paginator_list(method):
    """
    对某个查询结果进行分页,自带jsonp
    标准的分页器
    :param method:
    :return:
    """

    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        # callback = self.get_argument('callback', None)
        page_idx = self.get_argument('page_idx', '1')  # 页面索引号-var
        page_cap = self.get_argument('page_cap', '15')  # 一页的记录容量-var

        page_idx = int(page_idx)
        page_cap = int(page_cap)

        my_paginator_data = await method(self, *args, **kwargs)

        if my_paginator_data is None:
            rcs_len = 0
            my_paginator_data = []
        else:
            rcs_len = len(my_paginator_data)  # 记录总长度

        # 前端分页显示的内容
        page_total_cnts = int(math.ceil(rcs_len / page_cap))  # 页面的总数

        # 计算分页数据
        start_idx = (page_idx - 1) * page_cap  # 起始记录

        end_idx = start_idx + page_cap
        if end_idx > rcs_len:
            end_idx = rcs_len  # 防止溢出

        page_data = my_paginator_data[start_idx:end_idx]  # 取出分页的数据

        res_dict = dict(
            page_total_cnts=page_total_cnts,
            page_idx=page_idx,
            page_cap=page_cap,
            page_data=page_data,
        )

        res_str = jsontool.dumps(res_dict, ensure_ascii=False)
        return res_str

    return wrapper
