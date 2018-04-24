"""
mogodb的文档基类
"""
import datetime
# from aiomotorengine import Document, StringField, DateTimeField, BooleanField
# from aiomotorengine import IntField

from dtlib.timetool import get_current_utc_time, get_current_time


def wrap_default_rc_tag(origin_dict):
    """
    直接使用motor的时候,对dict外包一层默认tag
    :return:
    """
    now_time = get_current_utc_time()
    origin_dict.update(rc_time=now_time)
    origin_dict.update(is_del=False)
    origin_dict.update(del_time=now_time)
    return origin_dict


# class MyDocument(Document):
#     """
#     作为一道简单地封装，一些基本要素,数据记录本身的信息
#     """
#     rc_time = DateTimeField()  # 记录创建时间record create time
#     is_del = BooleanField()  # 是否删除,实际上数据不会被真正删除掉
#     del_time = DateTimeField()  # 记录删除时间
#
#     def set_default_rc_tag(self):
#         """
#         设置默认的数据记录标记，utc0时区
#         """
#         now_time = get_current_utc_time()  # 只要是涉及到mongodb中的时间储存全部都用utc时间
#         self.rc_time = now_time
#         self.is_del = False
#         self.del_time = now_time
#
#     def set_default_local_rc_tag(self):
#         """
#         设置默认的当前时区的一些标记
#         :return:
#         """
#         now_time = get_current_time()  # 只要是涉及到mongodb中的时间储存全部都用utc时间
#         self.rc_time = now_time
#         self.is_del = False
#         self.del_time = now_time
#
#     def set_template(self):
#         """
#         设置默认模板,如果用户不填写这些，则可以填写一些默认的数据
#         :return:
#         """
#         pass
#
#     def get_id(self):
#         """
#         获取id
#         :return:
#         """
#         return self._id
#
#     def set_id(self, id):
#         """
#         设置id
#         :param id:
#         :return:
#         """
#         self._id = id
#
#     def to_dict(self):
#         """
#         转化为带id的dict,方便jsontool.dumps
#         替代_values
#         :return:
#         """
#         data = self.to_son()
#         data.update(id=self._id)
#         return data
#
#     async def safety_del(self):
#         """
#         安全删除:只置相应标志位
#         :return:
#         """
#         self.is_del = True
#         self.del_time = get_current_utc_time()
#         return await self.save()
#
#     async def save_with_tag(self):
#         """
#         带上时间标记的save
#         :return:
#         """
#         self.set_default_rc_tag()
#         return await self.save()
#
#     async def complete_del(self):
#         """
#         完全删除掉记录
#         :return:
#         """
#         return await super(MyDocument, self).delete()
#
#     async def delete(self):
#         """
#         子类重写父类函数
#         安全删除:只置相应标志位
#         :return:
#         """
#         self.is_del = True
#         self.del_time = get_current_utc_time()
#         return await self.save()
#         # await super(MyDocument, self).save()
#
#
# class HttpDocument(Document):
#     """
#     带Http头部信息的
#     """
#     ip = StringField()  # 用户登陆ip
#     user_agent = StringField()  # 移动端的UA
#     cookie = StringField()
#     referrer = StringField()  # referer
#
#     def set_http_tag(self, **kwargs):
#         """
#         设置http的标记
#         :return:
#         """
#         http_req = kwargs.get('http_req', None)
#         """:type MyBaseHandler"""
#         http_request = http_req.request
#         self.ip = http_request.remote_ip  # 客户端访问的IP
#         self.user_agent = http_request.headers.get('User-Agent', None)
#         self.cookie = http_request.headers.get('Cookie', None)
#         self.referrer = http_request.headers.get('Referer', None)
#
#
# class OperationDocument(Document):
#     """
#     操作记录的文档
#     """
#     o_type = IntField()  # 用户的操作类型operate type,登录,参见常量:LogConst
#     o_name = StringField(max_length=32)  # 操作名称，冗余
#
#     def set_operation_tag(self, **kwargs):
#         """
#         设置操作标记
#         :return:
#         """
#
#         operation_dict = kwargs.get('operation', None)
#         """:type:ValueDict"""
#
#         if operation_dict is None:
#             return None
#
#         self.o_type = operation_dict.value
#         self.o_name = operation_dict.key
#
#
# class ClientTypeDocument(Document):
#     """
#     带客户端类型的文档
#     """
#     c_type = IntField()  # client type
#     c_name = StringField()  # client name 冗余
#
#     def set_client_type_tag(self, **kwargs):
#         """
#         设置客户端标记
#         :return:
#         """
#
#         client_dict = kwargs.get('client_type', None)
#         """:type:ValueDict"""
#
#         if client_dict is None:
#             return None
#
#         self.c_type = client_dict.value
#         self.c_name = client_dict.key
