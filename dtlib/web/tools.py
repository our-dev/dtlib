"""
tornado 相关的工具库
"""
import shlex
import subprocess

from tornado.gen import coroutine, Task, Return
from tornado.process import Subprocess

from dtlib import jsontool
from dtlib.utils import list_have_none_mem
from dtlib.web.constcls import ConstData


@coroutine
def call_subprocess(cmd, stdin_data=None, stdin_async=True):
    """异步进行系统调用，call sub process async
        Args:
            cmd: str, commands
            stdin_data: str, data for standard in
            stdin_async: bool, whether use async for stdin
    """
    stdin = Subprocess.STREAM if stdin_async else subprocess.PIPE
    sub_process = Subprocess(shlex.split(cmd),
                             stdin=stdin,
                             stdout=Subprocess.STREAM,
                             stderr=Subprocess.STREAM, )

    if stdin_data:
        if stdin_async:
            yield Task(sub_process.stdin.write, stdin_data)
        else:
            sub_process.stdin.write(stdin_data)

    if stdin_async or stdin_data:
        sub_process.stdin.close()

    result, error = yield [Task(sub_process.stdout.read_until_close),
                           Task(sub_process.stderr.read_until_close), ]

    raise Return((result, error))


def get_std_json_response(**kwargs):
    """
    获取标准的json返回值,以此处为标准,传入的参数：

    - code:整数
    - msg:字符串提示
    - data：json字符串,不能为空

    从2017-04-07之后推荐使用get_std_json_res函数替代

    :return:
    """
    code = kwargs.get('code', 200)
    msg = kwargs.get('msg', '')
    data = kwargs.get('data', '')
    #
    # if list_have_none_mem(*[code, msg, data]) is True:
    #     raise ValueError

    # res_dict = dict(
    #     code=code,
    #     msg=msg,
    #     data=data
    # )
    # return jsontool.dumps(res_dict)
    return ConstData.res_tpl % (code, msg, data)


def get_std_json_res(**kwargs):
    """
    获取标准的json返回值,以此处为标准,传入的参数：

    - code:整数
    - msg:字符串提示
    - data：传进来的是dict，不是str类型

    :return:
    """
    code = kwargs.get('code', 200)
    msg = kwargs.get('msg', '')
    data = kwargs.get('data', '')

    if list_have_none_mem(*[code, msg, data]) is True:
        raise ValueError

    res_dict = dict(
        code=code,
        msg=msg,
        data=data
    )
    return jsontool.dumps(res_dict, ensure_ascii=False)


def get_jsonp_res(callback, origin_res):
    """
    将普通返回值转化为jsonp
    :param callback:
    :param origin_res:
    :return:
    """
    if callback is None:
        return origin_res
    else:
        res = '%s(%s)' % (callback, origin_res)
        return res


if __name__ == '__main__':
    res_dict = dict(
        x_pos=56
    )
    print(res_dict)
    print(get_std_json_res(data=res_dict))

    print('run end')
