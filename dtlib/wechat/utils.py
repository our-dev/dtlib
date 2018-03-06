# coding:utf-8
import hashlib

__author__ = 'zheng'



def base_check_signature(signature, timestamp, nonce, token='weixin_api_token'):
    """ 微信token校验，接口认证
    :param signature:
    :param timestamp:
    :param nonce:
    :param token:
    :return:
    """
    args = []
    args.append(token)
    args.append(timestamp)
    args.append(nonce)
    args.sort()
    mysig = hashlib.sha1(''.join(args)).hexdigest()
    return mysig == signature