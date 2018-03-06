"""
jenkins的API
"""

import jenkins
from dtlib.dtlog import dlog


class MyJenkins(object):
    def __init__(self, **kwargs):
        self.token = kwargs.get('token', '')  # 用于webhook认证的token
        self.listen_branch = kwargs.get('listen_branch', 'master')  # 监听构建的分支名称
        self.url = kwargs.get('url', '')
        self.user = kwargs.get('user', '')
        self.passwd = kwargs.get('passwd', '')

    def build(self, project_name):
        """
        触发项目构建
        提供了阻塞的方式
        :param project_name:
        :return:
        """
        jen = jenkins.Jenkins(self.url, username=self.user, password=self.passwd)
        jen.build_job(project_name)
        dlog.debug("build %s succeed" % project_name)
