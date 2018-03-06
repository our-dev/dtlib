# coding:utf-8
"""
some object may not serial by json lib,then enhenced it
从jsondate里面copy的模板，加入了：

1. ObjectId的序列化,
datetime 加入时区
"""

import datetime
import json

# from bson import ObjectId
from bson import ObjectId

DATE_FMT = '%Y-%m-%d'
ISO8601_FMT = '%Y-%m-%dT%H:%M:%SZ'
HUMAN_FMT = '%Y-%m-%d %H:%M:%S'  # 日常人们使用的格式


def _datetime_encoder(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime(HUMAN_FMT)
    elif isinstance(obj, datetime.date):
        return obj.strftime(DATE_FMT)
    elif isinstance(obj, ObjectId):
        return str(obj)

    raise TypeError


def _datetime_decoder(dict_):
    for key, value in dict_.items():
        # The built-in `json` library will `unicode` strings, except for empty
        # strings which are of type `str`. `jsondate` patches this for
        # consistency so that `unicode` is always returned.
        if value == '':
            dict_[key] = u''
            continue

        try:
            datetime_obj = datetime.datetime.strptime(value, ISO8601_FMT)
            dict_[key] = datetime_obj
        except (ValueError, TypeError):
            try:
                date_obj = datetime.datetime.strptime(value, DATE_FMT)
                dict_[key] = date_obj.date()
            except (ValueError, TypeError):
                continue

    return dict_


def dumps(*args, **kwargs):
    kwargs['default'] = _datetime_encoder
    return json.dumps(*args, **kwargs)


def dump(*args, **kwargs):
    kwargs['default'] = _datetime_encoder
    return json.dump(*args, **kwargs)


def loads(*args, **kwargs):
    kwargs['object_hook'] = _datetime_decoder
    return json.loads(*args, **kwargs)


def load(*args, **kwargs):
    kwargs['object_hook'] = _datetime_decoder
    return json.load(*args, **kwargs)
