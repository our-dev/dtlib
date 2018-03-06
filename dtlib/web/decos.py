import functools


def my_jsonp(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        �~P~L步Jsonp�~L~E�~E
        :param self:
        :type self: BaseHandler
        :param args:
        :param kwargs:
        :return:
        """
        callback = self.get_argument('callback', None)
        if callback is None:
            res_str = method(self, *args, **kwargs)
        else:
            res = method(self, *args, **kwargs)
            res_str = '%s(%s)' % (callback, res)
        self.write(res_str)

    return wrapper

def deco_jsonp(is_async=True):
    """
    针对全网的接口的使用量的统计
    :param is_async: 
    :return: 
    """

    def _jsonp(method):
        """
        带参数，综合了同步和异步的装饰器，必须带参数
        :param method:
        :return:
        """

        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            """
            :type self MyBaseHandler
            """
            callback = self.get_argument('callback', None)

            if is_async:
                res = await method(self, *args, **kwargs)
            else:
                res = method(self, *args, **kwargs)

            if callback is not None:
                res = '%s(%s)' % (callback, res)
            self.write(res)

        return wrapper

    return _jsonp
