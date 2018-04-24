"""
一些通用的web开发时使用到的类
"""

# from aiomotorengine import StringField, IntField, ReferenceField, BooleanField

# from dtlib.aio.base_mongo import MyDocument, OperationDocument, ClientTypeDocument, HttpDocument
from dtlib.dtlog import dlog
# from dtlib.tornado.base_docs import OrgUserDataDocument, UserBaseDocument, OrgBaseDocument
from dtlib.utils import list_have_none_mem


# class ApiCallCounts(MyDocument):
#     """
#     Api的的调用次数
#     """
#     __collection__ = "api_call_counts"
#     api_name = StringField()  # API的名称调用统计
#     counts = IntField()  # 调用次数
#     # organization = ReferenceField(reference_document_type=Organization)  # 数据所属的组织


#
# class HttpRequestHead(MyDocument):
#     """
#     浏览器请求头部信息-http://djangobook.py3k.cn/appendixH/
#     后面并没有什么用了：2016-05-31
#     """
#     content_length = StringField(max_length=32)
#     content_type = StringField(max_length=256)
#     query_string = StringField(max_length=102400000)
#     remote_addr = StringField(max_length=16)
#     remote_host = StringField(max_length=128)
#     server_name = StringField(max_length=128)
#     server_port = StringField(max_length=128)
#
#     http_accept_encoding = StringField(max_length=256)
#     http_accept_language = StringField(max_length=256)
#     http_host = StringField(max_length=32)
#     http_referer = StringField(max_length=10240)
#     http_user_agent = StringField(max_length=512)
#     http_x_bender = StringField(max_length=1024)
#     request_method = StringField(max_length=128)
#     # cookies = DynamicField()

# class ApiCallLog(MyDocument):
#     """
#     Api的的调用日志记录-对日常行为进行记录,
#     XX用户执行了XX操作,目前只对登入登出做了限制
#     """
#     __collection__ = "api_call_log"
#
#     user_id = ReferenceField(reference_document_type=User)
#     func_code_file_name = StringField(max_length=256)  # 函数文件路径
#     func_code_first_line_no = IntField()  # 函数所在行
#     func_name = StringField(max_length=256)  # 函数名称
#     # log_msg = StringField()  # API的调用统计
#     http_request_head = EmbeddedDocumentField(HttpRequestHead)


# class OrgApiCallCounts(OrgUserDataDocument):
#     """
#     组织内的用户的Api的的调用次数,具体到了用户的信息粒度
#     """
#     __collection__ = "org_api_call_counts"
#     api_name = StringField()  # API的名称调用统计
#     counts = IntField()  # 调用次数
#
#
# class TestDataApp(OrgBaseDocument):
#     """
#     - 创建一个web应用，供客户端来调用,和测试相关的api应用的接口
#     - APP是属于组织的
#     - 自动化的接口
#     """
#
#     __collection__ = "test_data_app"
#     __lazy__ = False  # 直接全部查询出来
#
#     app_id = StringField(max_length=32)  # 对应的id,uuid1生成,要求唯一性
#     app_key = StringField(max_length=32)  # 相应的key值，使用随机的字符串乱序生成，不要求唯一性，只要求不好穷举
#     is_default = BooleanField()  # 是否是默认创建
#
#
# class OrgAppCallCounts(OrgBaseDocument):
#     """
#     组织的某个具体应用的接口调用次数
#     """
#     __collection__ = "org_app_call_counts"
#     __lazy__ = False
#     app = ReferenceField(reference_document_type=TestDataApp)
#     api_name = StringField()  # API的名称调用统计
#     counts = IntField()  # 调用次数
#
#
# class UserRegInfo(HttpDocument, UserBaseDocument):
#     """
#     用户在注册的时候，携带的一些附加的信息,例如iP,cookie，设备指纹等等
#     """
#     __collection__ = "user_reg_info"
#     __lazy__ = False
#
#     # todo 随着后续的安全功能增加，相关的信息也要收集
#     fprt = StringField()  # 设备指纹
#     pass
#
#
# class UserDetailInfo(UserBaseDocument):
#     """
#     用户的详细信息
#     """
#
#     __collection__ = "user_detail_info"
#     __lazy__ = False
#
#     phone = StringField()
#     email = StringField()
#     qq = StringField()
#     # todo 再有其它的继续加入
#
#
# class FeedBackMsg(UserBaseDocument):
#     """
#     内网应用的用户
#     """
#     __collection__ = "feedback_msg"
#     msg = StringField()  # 反馈的内容
#     label = StringField()  # 问题的标签分类
#
#
# class LogHistory(OrgUserDataDocument, OperationDocument, ClientTypeDocument, HttpDocument):
#     """
#     用户登录日志,带登录的
#     """
#     __collection__ = "log_history"
#
#     async def save_status(self, **kwargs):
#         """
#         保存当前状态
#         :return:
#         """
#
#         http_req = kwargs.get('http_req', None)  # http请求
#         """:type: MyBaseHandler"""
#
#         c_type = kwargs.get('client_type', None)
#         """:type:ValueDict"""
#         o_type = kwargs.get('operation', None)
#         """:type:ValueDict"""
#
#         if list_have_none_mem(*[http_req, c_type, o_type], ):
#             dlog.exception('you should have a  http request')
#             return None
#
#         await self.set_org_user_tag(http_req=http_req)
#
#         self.set_operation_tag(operation=o_type)
#         self.set_client_type_tag(client_type=c_type)
#         self.set_http_tag(http_req=http_req)
#         self.set_default_rc_tag()
#         await self.save()
