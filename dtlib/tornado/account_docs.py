"""
建立在用户和账号体系之上类
"""
from random import random

# from aiomotorengine import ReferenceField, StringField, IntField, FloatField, BooleanField, DateTimeField

# from dtlib.aio.base_mongo import MyDocument
from dtlib.tornado.status_cls import UserStatus, UserRegWay
from dtlib.utils import md5with_salt, hashlibmd5with_salt


# class User(MyDocument):
#     """
#     用于登录的用户
#     """
#     __collection__ = "g_users"
#     user_id = StringField()  # 账号ID,unique=True
#     passwd = StringField()  # 密码
#     salt = IntField()  # 防止别人md5撞库反向破解的随机数
#
#     nickname = StringField()  # 名
#     avatar = StringField()  # 用户头像链接
#
#     status = IntField()  # 1表示是可更改状态
#     active = BooleanField()
#     reg_way = IntField()  # 注册方式,见枚举类型UserRegWay
#
#     def set_template(self):
#         self.status = UserStatus.init
#         self.active = True
#         self.reg_way = UserRegWay.web
#
#     async def is_exist(self):
#         """
#         判断用户对象是否已经存在
#         :return:
#         """
#         if self.user_id is None:
#             return False
#         if self.user_id == '':
#             return True
#
#         obj = await User.objects.filter(unionid=self.unionid).find_all()
#
#         if obj is None:
#             return False
#
#         if len(obj) > 0:
#             return True
#         else:
#             return False
#
#     @classmethod
#     async def is_exist(cls, user_id):
#         """
#         判断是否已经存在此用户
#         :param user_id:
#         :return:
#         """
#         user = await User.objects.filter(user_id=user_id).find_all()
#         if user is None:
#             return True
#         return False
#
#     @classmethod
#     async def get_active_users(cls):
#         user = await User.objects.filter(active=True).find_all()
#         return user
#
#     @classmethod
#     def generate_salt(cls):
#         """
#         生成密码混淆数
#         :return:
#         """
#         return str(random(1, 500))
#
#     @classmethod
#     async def auth(cls, login_name, password):
#         user = await cls.objects.get(user_id=login_name)
#         if not user:
#             return False
#         md5_password = hashlibmd5with_salt(password, user.salt)
#         if md5_password == user.passwd:
#             return user
#         else:
#             return False
#
#     async def is_online(self):
#         """
#         判断是否在线
#         :return:
#         :rtype:bool
#         """
#         pass
#
#     async def get_by_obj_id(id_obj):
#         """
#         根据id的字符串来获取用户记录
#         :return:
#         """
#         return await User.objects.get(id=id_obj)
#         pass
#
#
# class UserDevice(MyDocument):
#     """
#     用户设备：
#     1. 邮箱
#     2. 手机
#     """
#
#     account = StringField()
#     d_type = IntField()  # 设备类型
#
#
# class MisWeChatUser(MyDocument):
#     """
#     Mis系统存储的第三方微信账号和备案
#     """
#     __collection__ = "wechat_user"
#     __lazy__ = False
#
#     user = ReferenceField(reference_document_type=User)  # 本系统的注册用户
#     appid = StringField()  # 由具体的微信应用ID创建产生的
#     openid = StringField(required=True)
#     nickname = StringField()  # 微信昵称
#     headimgurl = StringField()  # 头像图片链接,miniapp是avanta_url
#     province = StringField()
#     country = StringField()
#     city = StringField()
#     sex = IntField()  # 1表示男，女的是？,miniapp是gender
#     language = StringField()  # 语言
#     unionid = StringField(required=True)  # 同一个开发者，拥有同样的unionid
#
#     async def is_exist(self):
#         """
#         判断用户对象是否已经存在
#         :param cls:
#         :return:
#         """
#         if self.unionid is None:
#             self.unionid = ''
#         if self.appid is None:
#             self.appid = ''
#
#         user = await MisWeChatUser.objects.filter(
#             unionid=self.unionid,
#             appid=self.appid
#         ).find_all()
#
#         if len(user) > 0:
#             return True
#         else:
#             return False
#
#
# class Organization(MyDocument):
#     """
#     组织,公司，工作室
#     """
#
#     __collection__ = "organization"
#     __lazy__ = False
#
#     name = StringField()  # 组织名称
#     home_page = StringField()  # 公司主页
#     is_default = BooleanField()  # 是否是默认创建
#     owner = ReferenceField(reference_document_type=User)  # 拥有者,不以直接reference,循环引用
#     owner_name = StringField()  # 拥有者名称,冗余
#
#     @staticmethod
#     async def get_by_id(id):
#         """
#         根据id来查询
#         :return:
#         """
#         return await Organization.objects.get(id=id)
#
#     def set_template(self):
#         """
#         设置默认信息,但是仍然还需要配置一些别的信息才能正常，比如User
#         :return:
#         """
#         self.name = 'group template'  # 默认组织名称和用户昵称一样,后面提供修改接口
#         self.home_page = 'http://www.my-org-page.org'
#
#
# class UserOrgRelation(MyDocument):
#     """
#     用户和组织关系:多对多
#     这里面的_id，就是映射关系的ID，是唯一的，可以作为用户在此组织下的ID，作为组织的返回值
#     """
#     __collection__ = "user_org_rel"
#
#     __lazy__ = False  # 直接全部查询出来
#
#     user = ReferenceField(reference_document_type=User)
#     user_name = StringField()  # 账号昵称,冗余
#     organization = ReferenceField(reference_document_type=Organization)  # 所属于组织
#     org_name = StringField()  # 组织名称,冗余
#     is_current = BooleanField()  # 是否是当前组织,具有排它性
#     is_owner = BooleanField()  # 用户是否是当前组织的所有者,具有排它性
#     is_default = BooleanField()  # 是否由系统默认创建,为了方便用户快速使用系统,用户进入后就直接建立组织
#     is_active = BooleanField()  # 是否审核通过,被激活
#
#
# class UserRegInviteRelation(MyDocument):
#     """
#     用户注册邀请关系
#     """
#     __collection__ = 'user_reg_invite_rel'
#
#     host = ReferenceField(reference_document_type=User)  # 主邀请人
#     host_name = StringField()  # 冗余
#     guest = ReferenceField(reference_document_type=User)  # 被邀请人
#     guest_name = StringField()  # 冗余
#
#
# class UserRegInviteCode(MyDocument):
#     """
#     用户注册码及统计
#     """
#
#     __collection__ = 'user_reg_invite_code'
#
#     host = ReferenceField(reference_document_type=User)  # 主邀请人用户
#     invite_code = StringField(unique=True, required=True)  # 邀请码,使用uuid1生成
#     get_cnt = IntField()  # 请求数
#     reg_cnt = IntField  # 请求后成功注册数
#     ratio = FloatField()  # 转化率,冗余的,百分号的分母位
