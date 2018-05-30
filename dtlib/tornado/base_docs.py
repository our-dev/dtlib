"""
基础的基类，一定会被继承的类
"""
# from aiomotorengine import StringField, DateTimeField, IntField, ReferenceField, Document
from dtlib import randtool

# from dtlib.aio.base_mongo import MyDocument, HttpDocument
# from dtlib.tornado.account_docs import User, Organization


# class BaseToken(MyDocument, HttpDocument):
#     """
#     基本token，不带user信息的
#     """
#
#     token = StringField(max_length=1024,
#                         # unique=True,#在3.4的server当中会有问题
#                         required=True)
#     """令牌为用户登录返回 后续操作必须提交参数 用户退出前不改变 每次登录生成"""
#
#     last_use_time = DateTimeField(required=True)  # 最后使用的时间
#
#     #
#     finger_prt = StringField()  # 设备指纹
#
#     c_type = IntField()  # 客户端类型:有数据字典查询
#     c_name = StringField()  # 客户端类型描述，冗余方便查看,client name
#
#     def set_uuid_rand_token(self):
#         """
#         生成一组Token,40位的,32位的uuid，和8byte的随机数，被归纳枚举的可能性是
#         :return:
#         """
#         self.token = randtool.generate_uuid_token()
#
#     def set_uuid_token(self):
#         """
#         生成唯一的32位码，如果在不用担心枚举的场合
#         :return:
#         """
#         self.token = randtool.get_uuid1_key()
#
#
# class OrgBaseField(Document):
#     """
#     组织信息字段
#     """
#     organization = ReferenceField(reference_document_type=Organization)  # 数据所属的组织
#     o_name = StringField()  # 组织名称，冗余
#
#     async def set_org_tag(self, http_req):
#         """
#         打上项目标记
#         :type http_req:MyBaseHandler
#         :return:
#         """
#
#         current_org = await http_req.get_organization()
#         """:type:Organization"""
#
#         self.organization = current_org
#         self.o_name = current_org.name
#
#
# class UserBaseField(Document):
#     """
#     用户信息字段
#     """
#     user = ReferenceField(reference_document_type=User)  # 测试数据所属的项目
#     u_name = StringField()  # 用户名称,冗余
#
#     def set_user_tag(self, http_req):
#         """
#         打上项目标记
#         :type http_req:MyBaseHandler
#         :return:
#         """
#
#         current_user = http_req.get_current_session_user()
#         """:type:User"""
#
#         self.user = current_user
#         self.u_name = current_user.nickname


# class UserToken(UserBaseField, BaseToken):
#     """
#     所有的和token相关的一些类,带用户信息的
#     """
#
#     # __lazy__ = False#本设置不能被继承
#
#     @classmethod
#     async def is_active(cls, token):
#         """
#         通过token,判定是否是激活态:
#
#         1. 存在记录
#         2. 而且记录中有用户名称作为签名
#         :return:
#         """
#
#         my_token = await cls.objects.get(token=token)
#         """:type:UserToken"""
#         if my_token is None:
#             return False
#
#         if my_token.user is None:
#             return False
#
#         return True
#
#     def set_user_tag(self, http_req):
#         """
#         :param http_req: MyOriginBaseHandler
#         :return:
#         """
#         user = http_req.get_current_session_user
#         self.user = user
#         self.u_name = user.name


class StatusBaseDocument(object):
    """
    所有状态量的基类
    """

    init = 0  # 初始值
    finish = 1  # 完成态


# class OrgBaseDocument(OrgBaseField, MyDocument):
#     """
#     组织的数据信息
#     """
#     pass
#
#
# class UserBaseDocument(UserBaseField, MyDocument):
#     """
#     带上了用户信息
#     """
#     # 数据归属
#     pass
#
#
# class UserOrgBaseDocument(UserBaseField, OrgBaseField, MyDocument):
#     """
#     带上了用户，组织，时间标记信息
#     """
#
#     async def set_org_user_tag(self, **kwargs):
#         """
#         保存组织和用户的数据标记
#         # 设置组织和人员归属关系
#         :type http_req
#         :return:
#         """
#         http_req = kwargs.get('http_req', None)
#         """:type: MyOriginBaseHandler"""
#
#         org = await http_req.get_organization()
#         user = http_req.get_current_session_user()
#         self.set_default_rc_tag()
#         self.set_user_tag(user)
#         self.set_org_tag(org)


# todo notice :下面的3个用户组织的基础，在2017-05-26之后，尽量再新建代码中使用，尽量使用上面的类

# class OrgDataBaseDocument(Document):
#     """
#     带有组织信息标记的数据：基类。
#     后面推荐使用：OrgBaseDocument 以简化字段名
#     - 2017-05-26
#     """
#     organization = ReferenceField(reference_document_type=Organization)  # 所属于组织
#     org_name = StringField()  # 组织名称,冗余
#
#     def set_org_tag(self, organization):
#         """
#         打上组织标记
#         :type organization:Organization
#         :return:
#         """
#         self.organization = organization
#         self.org_name = organization.name
#
#
# class UserDataBaseDocument(Document):
#     """
#     带有用户信息标记的数据：基类
#     warning:后面逐渐不再使用，推荐使用：UserBaseDocument替代，2017-5-31
#     """
#     owner = ReferenceField(reference_document_type=User)  # 所属用户
#     owner_name = StringField()  # 用户名称,冗余
#
#     def set_user_tag(self, user):
#         """
#         设置用户标记
#         :type user:User
#         :return:
#         """
#         self.owner = user
#         self.owner_name = user.nickname


# class OrgUserDataDocument(OrgDataBaseDocument, UserDataBaseDocument, MyDocument):
#     """
#     组织内用户数据，有如下特点：
#
#     1. 组织信息
#     2. 有用户信息
#     3. 默认的Document信息
#
#
#     - 后面再建立类时，用 UserOrgBaseDocument替代
#     - 2017-05-26
#     """
#
#     async def set_org_user_tag(self, **kwargs):
#         """
#         保存组织和用户的数据标记
#         # 设置组织和人员归属关系
#         :type http_req
#         :return:
#         """
#         http_req = kwargs.get('http_req', None)
#         """:type: MyOriginBaseHandler"""
#
#         org = await http_req.get_organization()
#         assert org is not None, 'Current user have no organization relation'
#         user = http_req.get_current_session_user()
#         self.set_default_rc_tag()
#         self.set_user_tag(user)
#         self.set_org_tag(org)
