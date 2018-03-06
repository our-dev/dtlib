#!coding:utf8
from distutils.core import *

import dtlib

current_version = dtlib.VERSION

if __name__ == '__main__':
    with open('requirements.txt') as f:
        required = f.read().splitlines()

    setup(
        name='dtlib',
        version=current_version,
        # version='2.15.9.25.1',
        packages=[
            'dtlib',
            'dtlib.aio',
            'dtlib.mongo',
            'dtlib.tornado',
            'dtlib.web',
            'dtlib.wechat',

        ],
        url='http://www.bitbucket.com',
        license='',
        author='Simon',
        author_email='1295351490@qq.com',
        description='self debug and testing',
        install_requires=required,

    )
