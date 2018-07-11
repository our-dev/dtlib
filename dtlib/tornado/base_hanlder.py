import hashlib
import json

from tornado.web import RequestHandler

from dtlib.timetool import get_current_utc_time
# from dtlib.tornado.account_docs import UserOrgRelation, Organization
from dtlib.tornado.const_data import FieldDict
# from dtlib.tornado.docs import TestDataApp, LogHistory
# from dtlib.tornado.ttl_docs import AppSession, AccessToken
from dtlib.utils import list_have_none_mem
from dtlib.web.constcls import QrAuthStatusCode
from dtlib.web.valuedict import ClientTypeDict, OperationDict

from dtlib.tornado.utils import set_default_rc_tag
from dtlib import randtool
from bson import ObjectId


class SessionKey(object):
    """
    存储session的时候key值常量定义
    """
    user = 'user'
    """用户对象"""
    test_web_app = 'test_web_app'
    """测试web的应用"""
    login_status = 'login_status'
    """登录状态"""


class BaseHandler(RequestHandler):
    """自定义的基类,基于torndsession的,因为没有redis的异步库,所以比较有限

    session的字段：

    - user:用户对象WechatUser
    - login_status：登录状态

    """

    #
    # def __init__(self):
    #     self.sessionid = ''
    #     self.username = ''

    def get_user(self):
        """
        获取当前登录用户
        :return:
        :rtype: WechatUser
        """
        user = self.session.get(SessionKey.user, None)
        if user is None:
            return None
        return user

    def set_user(self, login_user):
        """
        :return:
        """
        self.session.set(SessionKey.user, login_user)

    def get_test_data_app(self):

        test_web_app = self.session.get(SessionKey.test_web_app, None)
        if test_web_app is None:
            return None
        return test_web_app

    def set_test_data_app(self, test_web_app):
        """
        设置当前web应用的session
        :param test_web_app:
        :return:
        """
        self.session.set(SessionKey.test_web_app, test_web_app)

    def get_login_status(self):
        """
        获取登录用户状态
        :return:
        """
        login_status = self.session.get(SessionKey.login_status, None)
        if login_status is None:
            return None
        return login_status

    def set_login_status(self, status):
        """
        获取登录用户状态
        :return:
        """
        self.session.set(SessionKey.login_status, status)

    def get_context(self, **kwargs):
        """
        添加一些通用的上下文应用
        """
        kwargs.update(
            login_user=self.session.get(SessionKey.user),  # 登录的用户
            # perms=self.session.get('perms',None)  # 用户的权限
        )

        return kwargs

    def prepare(self):
        pass

    def set_wechat_auth_sesstion(self, **kwargs):
        """
        设置微信登录后的session
        """
        user_info = kwargs.get('wechat_user', None)
        if user_info is not None:
            self.set_user(user_info)
            self.set_login_status(True)
            # self.session.set('user', user_info)
            # self.session.set('login_status', True)


class MyOriginBaseHandler(RequestHandler):
    """
    自定义session的类,基于tornado的

    - logsession是登录的token,使用mongodb来存储
    - sessionid使用redis来存储,以后用token,不用session了

    """

    def __init__(self, *args, **kwargs):
        super(MyOriginBaseHandler, self).__init__(*args, **kwargs)
        # self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-type, Accept, connection, User-Agent, Cookie')
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS')
        self.set_header('Content-Type', 'application/json')
        self.set_header('charset', 'utf-8')

        self.token = None  # API中用于做身份认证的内容,相当于sessionid
        self.cache_session = None  # 用token取一次之后的session的缓存,是一个log_session的对象
        """:type:BaseToken"""

    def get_post_body_dict(self):
        """
        获取post的body中的json内容
        :return:
        """
        post_byte = self.request.body
        if len(post_byte) == 0:
            return {}
        post_str = str(post_byte, encoding="utf-8")
        json_res = json.loads(post_str)
        return json_res

    async def get_async_redis(self):
        """
        获取redis的连接池,从settings里面处理
        :return:
        """
        rc_pool = self.settings.get(FieldDict.key_async_redis_pool, None)
        assert rc_pool is not None
        # conn = await rc_pool.get()
        with (await rc_pool) as coon:
            return coon

    def get_sync_redis(self):
        """
        获取同步redis的连接池
        :return:
        """
        rc_pool = self.settings.get(FieldDict.key_sync_redis_pool, None)
        assert rc_pool is not None

        return rc_pool

    def get_async_mongo(self):
        """
        获取异步的连接
        :return:
        """
        mc_pool = self.settings.get(FieldDict.key_async_mongo_pool, None)
        assert mc_pool is not None
        return mc_pool

    async def set_session_by_token(self, cookie_enable=False):
        """
        根据http请求来检查token是否有效:
        1. 从get中获取
        2. 从post中获取
        3. 从cookie中获取（可选）
        :param self: 
        :param cookie_enable: 
        :return: 
        """
        pass

    def get_token(self):
        return self.token

    async def log_out(self):
        """
        登出系统,删除对应的session
        :return:
        """
        log_session = self.cache_session

        mongo_conn = self.get_async_mongo()
        token_col = mongo_conn['ttl_access_token']

        token_res = await token_col.find_one(log_session)
        # if token_res:
        #     print("1", token_res)

        if log_session is not None:
            await token_col.remove(log_session)

    async def get_organization(self):
        """
        获取当前用户 或者 当前应用的用户
        具体由子类中定义
        :return:
        """
        pass


class MyUserBaseHandler(MyOriginBaseHandler):
    def __init__(self, *args, **kwargs):
        super(MyOriginBaseHandler, self).__init__(*args, **kwargs)
        self.cache_session = None  # App用于登录的session
        """:type:UserToken"""

    async def set_session_by_token(self, cookie_enable=False):
        """
        根据http请求来检查token是否有效:
        1. 从get中获取
        2. 从post中获取
        3. 从cookie中获取（可选）
        :param self: 
        :param cookie_enable: 
        :return: 
        """
        token = self.get_argument('token', None)

        if token is None:
            post_json = self.get_post_body_dict()
            token = post_json.get('token', None)

        if (token is None) and cookie_enable:
            token = self.get_cookie('token', None)

        if token is None:
            return None

        mongo_conn = self.get_async_mongo()
        # todo: extract collection name
        token_col = mongo_conn['ttl_access_token']

        log_session = await token_col.find_one({'token': token, 'is_del': False})

        # log_session = await AccessToken.objects.get(token=token)
        # """:type:AccessToken"""

        if log_session is None:
            return None

        # 在此处直接赋值存储session,一些临时变量在此处缓存
        self.token = token  # 本次请求都会用到token,相当于会话标识
        self.cache_session = log_session

        self.set_cookie('token', self.token)

        return log_session

    def get_current_session_user(self):
        """
        获取当前用户对象,从session中获取
        :return:
        :rtype:User
        """
        user = self.cache_session['user']
        return user

    async def get_organization(self):
        """
        获取当前组织名称,根据用户,默认的缺省组织
        :return:
        :rtype:Organization
        """
        # user_id = await self.get_user_id()
        # user = await User.objects.get(user_id=user_id)
        user = self.cache_session['user']
        #
        # if user is None:
        #     return None

        db = self.get_async_mongo()
        rel_col = db.user_org_rel
        # todo: is_del?
        current_rels = await rel_col.find_one({
            'user': ObjectId(user),
            'is_current': True,
            'is_active': True
        })

        # current_rels = await UserOrgRelation.objects.filter(user=user, is_current=True, is_active=True).find_all()
        # """:type:list[UserOrgRelation]"""

        if current_rels is None:
            return None

        # len_rels = len(current_rels)
        # if len_rels == 0:
        #     msg = 'Exception:no active or current orgnizations,please contact the admin'
        #     print(msg)
        #     return None
        #
        # if len_rels > 1:
        #     msg = 'Exception:more than one current data,please contact the admin'
        #     print(msg)
        #     return None
        #
        # current_rels = current_rels[0]

        return current_rels['organization']

    async def create_token_session(self, user, **kwargs):
        """
        区别：加入了 平台的描述
        创建 或者 刷新 token,
        包括各种 ttl_token
    
        现在是进行了扩展了,所以用这种方式,
    
        - 允许有匿名的存在
    
        :type self:MyBaseHandler
        :type cls:UserToken
        :type user:User
        :param client_type: 客户端类型
        :return:
        :rtype:UserToken
        """

        client_type = kwargs.get('client_type', None)  # 默认的是浏览器端
        """:type:ValueDict"""
        # cls = kwargs.get('token_cls', None)
        # """:type:UserToken"""

        if list_have_none_mem(*[client_type]):
            return None
        # 读取 mongodb，获取用户对应的 token，单点登录情况下使用
        # my_token = await cls.objects.get(user=user, c_type=client_type.value)
        """:type:WebToken"""

        ip = self.request.remote_ip
        user_agent = self.request.headers['User-Agent']
        finger_prt = hashlib.md5(user_agent.encode("utf-8")).hexdigest()

        # # if my_token is None:  # 单点登录情况下使用
        # my_token = cls(
        #     c_type=client_type.value,
        #     c_name=client_type.key,
        # )
        # """:type:UserToken"""

        db = self.get_async_mongo()
        token_col = db['ttl_access_token']
        user_col = db['g_users']

        user_res = await user_col.find_one({'_id': user})

        if not user_res:
            return None
        new_token = dict(
            user=user_res['_id'],
            # todo: save user_id
            u_name=user_res['nickname']
        )

        # if user is not None:
        #     my_token.user = user.get_id()
        #     my_token.u_name = user.nickname

        # 允许有匿名用户的存在,这个时候就表明没有被签名的匿名登录
        new_token = set_default_rc_tag(new_token)
        new_token['token'] = randtool.generate_uuid_token()
        new_token['last_use_time'] = get_current_utc_time()
        new_token['ip'] = ip
        new_token['user_agent'] = user_agent
        new_token['finger_prt'] = finger_prt
        # my_token = await my_token.save()  # 通过save获取的my_token并没有lazy出来，后面赋值的时候会有影响
        # """:type:UserToken"""
        #
        # my_token = await cls.objects.get(id=my_token.get_id())  # 相当于使用了 loadReference功能

        await token_col.insert_one(new_token)

        return new_token

    async def create_anonymous_token(self, cls, **kwargs):
        """
        创建匿名token，主要用途：

        1. PC上生成二维码，给手机上扫码认证
        :param cls:
        :param kwargs:
        :return:
        """
        appid = kwargs.get('appid', None)
        client_type = kwargs.get('client_type', None)  # 默认的是浏览器端
        if list_have_none_mem(*[client_type]):
            return None

        ip = self.request.remote_ip

        # referer='' if self.request.headers is None
        user_agent = self.request.headers['User-Agent']
        finger_prt = hashlib.md5(user_agent.encode("utf-8")).hexdigest()

        # 如果是手机认证PC，则直接创建匿名token
        my_token = cls(
            c_type=client_type.value,
            c_name=client_type.key,
            appid=appid,
        )
        """:type:BaseToken"""

        # todo 后续如果把应用的系统做好了，这个地方要做一次数据库IO查询处理的，判断是否存在，防止别人撞库

        # 允许有匿名用户的存在,这个时候就表明没有被签名的匿名登录
        my_token.set_default_rc_tag()
        my_token.status = QrAuthStatusCode.timeout

        my_token.set_uuid_rand_token()
        my_token.set_uuid_rand_token()  # 单点登录，将旧的token给弃用掉
        my_token.last_use_time = get_current_utc_time()
        my_token.ip = ip
        my_token.user_agent = user_agent
        my_token.finger_prt = finger_prt
        my_token = await my_token.save()
        """:type:UserToken"""

        return my_token

    def set_http_tag(self):
        """
        设置http的标记
        :return:
        """
        new_tag = dict(
            ip=self.request.remote_ip,  # 客户端访问的IP
            user_agent=self.request.headers.get('User-Agent', None),
            cookie=self.request.headers.get('Cookie', None),
            referrer=self.request.headers.get('Referer', None)
        )
        return new_tag

        # async def save_login_history(self, **kwargs):
        #     """
        #     保留登录记录
        #     :return:
        #     """
        #     # 登录记录里面增加一条记录
        #     # login_history = LoginHistory()
        #
        #     client_type = kwargs.get('client_type')
        #     """:type:ValueDict"""
        #     if list_have_none_mem(*[client_type]):
        #         return None
        #
        #     log_history = LogHistory()
        #     await log_history.save_status(
        #         http_req=self,
        #         client_type=client_type,
        #         operation=OperationDict.login)
        #
        # async def save_logout_history(self, **kwargs):
        #     """
        #     保留登录记录
        #     :return:
        #     """
        #     client_type = kwargs.get('client_type')
        #     """:type:ValueDict"""
        #     if list_have_none_mem(*[client_type]):
        #         return None
        #     log_history = LogHistory()
        #     await log_history.save_status(
        #         http_req=self,
        #         client_type=client_type,
        #         operation=OperationDict.logout)


class MyAppBaseHandler(MyOriginBaseHandler):
    """
    创建的应用程序的基类,应用程序都是以组织为基本单位的
    """

    def __init__(self, *args, **kwargs):
        super(MyAppBaseHandler, self).__init__(*args, **kwargs)
        self.cache_session = None  # App用于登录的session
        """:type:AppSession"""

    async def set_session_by_token(self, cookie_enable=True):
        """
        根据app的token获取session对象
        :return: 
        """
        token = self.get_argument('token', None)

        if token is None:
            post_json = self.get_post_body_dict()
            token = post_json.get('token', None)

        if (token is None) and cookie_enable:
            token = self.get_cookie('token', None)

        if token is None:
            return None

        db = self.get_async_mongo()
        session_col = db.ttl_app_session

        app_session = await session_col.find_one({'token': token})  # 使用token来表明是同一会话
        """:type:AppSession"""

        if app_session is None:
            return None

        # 在此处直接赋值存储session,一些临时变量在此处缓存
        self.token = app_session['token']  # 本次请求都会用到token,相当于会话标识
        self.cache_session = app_session

        self.set_cookie('token', self.token)

        return app_session

    async def create_app_session(self, app_id, **kwargs):
        """
        设置app的登录会话
        :return:
        """
        client_type = kwargs.get('client_type', ClientTypeDict.api)
        ip = self.request.remote_ip

        db = self.get_async_mongo()
        app_col = db.test_data_app
        session_col = db.ttl_app_session

        test_app = await app_col.find_one({'app_id': app_id})

        app_session = await session_col.find_one({'app_id': app_id})

        if app_session is not None:
            # 如果已经存在,则只需要更新时间
            current_time = get_current_utc_time()
            await session_col.update({'app_id': app_id},
                                     {'$set': {'last_use_time': current_time}})
            # app_session.last_use_time = get_current_utc_time()  # 更新在线时间
            # app_session = await app_session.save()
            app_session['last_use_time'] = current_time
            return app_session

        # 如果不存在登录状态记录,则重新创建session
        new_session = dict(
            app_id=app_id,
            c_type=client_type.value,
            c_name=client_type.key,
            organization=test_app['organization'],
            o_name=test_app['o_name'],
            ip=ip,
            token=randtool.generate_uuid_token(),
            last_use_time=get_current_utc_time()
        )
        new_session.update(self.set_http_tag())
        new_session = set_default_rc_tag(new_session)
        await session_col.insert_one(new_session)
        self.cache_session = new_session
        return new_session

    # async def get_app(self):
    #     """
    #     获取测试数据应用,根据当前session
    #     :return:
    #     """
    #     app_session = self.cache_session
    #     test_web_app = await TestDataApp.objects.get(app_id=app_session.app_id)
    #     if test_web_app is None:
    #         return None
    #     return test_web_app

    async def get_organization(self):
        """
        获取应用的组织信息
        :return:
        """

        try:
            organization = self.cache_session['organization']
        except:
            res = await self.cache_session.load_references(fields=['organization', ])
            # 一旦加载完成后，此值就一直保存在session中
            organization = res['loaded_values']['organization']
        return organization

    def set_http_tag(self):
        """
        设置http的标记
        :return:
        """
        new_tag = dict(
            ip=self.request.remote_ip,  # 客户端访问的IP
            user_agent=self.request.headers.get('User-Agent', None),
            cookie=self.request.headers.get('Cookie', None),
            referrer=self.request.headers.get('Referer', None)
        )
        return new_tag

#
#
# class MyBaseHandler(MyUserBaseHandler):
#     """
#     自定义session的类,基于tornado的
#
#     - logsession是登录的token,使用mongodb来存储
#     - sessionid使用redis来存储,以后用token,不用session了
#
#     """
#
#     def __init__(self, *args, **kwargs):
#         super(MyBaseHandler, self).__init__(*args, **kwargs)
#         # self.set_header('Access-Control-Allow-Origin', '*')
#         # self.set_header('Access-Control-Allow-Headers',
#         #                 'Origin, X-Requested-With, Content-type, Accept, connection, User-Agent, Cookie')
#         # self.set_header('Access-Control-Allow-Methods',
#         #                 'POST, GET, OPTIONS')
#
#     def set_http_tag(self):
#         """
#         设置http的标记
#         :return:
#         """
#         new_tag = dict(
#             ip=self.request.remote_ip,  # 客户端访问的IP
#             user_agent=self.request.headers.get('User-Agent', None),
#             cookie=self.request.headers.get('Cookie', None),
#             referrer=self.request.headers.get('Referer', None)
#         )
#         return new_tag
