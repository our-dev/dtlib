"""
一些具生命周期的ttl
"""
# from aiomotorengine import StringField, ReferenceField

# from dtlib.tornado.account_docs import Organization
# from dtlib.tornado.base_docs import UserToken, BaseToken, OrgBaseField, OrgBaseDocument


# class WebToken(UserToken):
#     """
#     用户登录会话,Web客户端的session
#
#     - 生存周期2天
#     - 通过账号和密码进行获取
#
#     """
#
#     __collection__ = "ttl_access_token"
#     __lazy__ = False
#
#
# class MobileToken(UserToken):
#     """
#     手机端的(mobile_token)refresh_token
#
#     - 生成周期为1年,过期删除（设置TTL）
#     - 代替账号和密码的保存,本地不保存账号和密码,减少账号密码被别人截取的机率
#     - 新终端登录后,旧的token就要被删除掉
#     用来获取统一的access_token
#     """
#     __collection__ = 'ttl_mobile_token'
#     __lazy__ = False
#
#
# class AccessToken(UserToken):
#     """
#     获取应用调用权限的token:
#
#     - 生存时间为2小时（设置TTL）
#     - 可以通过refresh_token来进行刷新时长
#     """
#     __collection__ = "ttl_access_token"
#     __lazy__ = False
#
#
# class AppSession(BaseToken, OrgBaseField):
#     """
#     自动化应用登录的session,这种高频接口要进行区分,失效时间也不一样
#     """
#
#     __collection__ = "ttl_app_session"
#     # __lazy__ = False
#     app_id = StringField(max_length=32, unique=True)
#
#
# class PcAuthMobileToken(UserToken):
#     """
#     由已经认证登录了的PC端生成的二维码的原始串号:（Waste）
#
#     - 移动端扫码后和用户信息关联
#     - 移动端获取refresh_token(长时效的)
#     - 根据 refresh_token 获取 access_token
#
#     备注:
#     - 生存周期为2分钟,2分钟后过期删除
#     - 没有被使用时,每1分钟变一次
#     - 被使用后,立刻删除掉
#     """
#
#     __collection__ = 'ttl_pam_token'
#     __lazy__ = False
#
#
# class TtlOrgInviteCode(OrgBaseDocument):
#     """
#     组织邀请码,邀请加入组织,有失效时间,由mongodb中设置ttl
#     """
#     __collection__ = "ttl_org_invite_code"
#     __lazy__ = False  # 直接全部查询出来
#
#     invite_code = StringField(unique=True, required=True)  # 邀请码,一个UUID
