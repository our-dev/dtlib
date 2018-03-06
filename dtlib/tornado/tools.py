# coding:utf-8
"""
tornado 相关的工具库
"""
import os
import shlex
import subprocess

from tornado.gen import coroutine, Task, Return
from tornado.process import Subprocess

from dtlib.dtlog import dlog
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

#
# def get_std_json_response(**kwargs):
#     """
#     获取标准的json返回值
#     :return:
#     """
#     code = kwargs.get('code', 200)
#     msg = kwargs.get('msg', '')
#     data = kwargs.get('data', '')
#     #
#     # if list_have_none_mem(*[code, msg, data]) is True:
#     #     raise ValueError
#     return ConstData.res_tpl % (code, msg, data)


def get_apps_url(base_dir):
    """
    find all the route.py under folder 'apps' and returns the url lists
    :param base_dir:根路径
    :return:
    """
    apps_url = []
    directory = os.path.join(base_dir, 'apps')
    try:
        for filename in os.listdir(directory):
            try:
                full_path = os.path.join(directory, filename)
                if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, 'urls.py')):
                    url_package_name = os.path.join('apps', filename, 'urls').replace('/', '.')
                    package_url_list = getattr(__import__(url_package_name, fromlist=['url']), 'url')
                    assert package_url_list is not None  # 原则上是不允许为空的
                    apps_url += package_url_list
            except Exception as e:
                dlog.exception('url-%s:%s' % (filename, e))
    except Exception as e:
        dlog.exception('url error:%s' % e)
    return apps_url


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    print(os.path.abspath('.'))
