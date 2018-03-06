# coding:utf-8
"""
和二维码相关的
"""
__author__ = 'zheng'

import qrcode

def get_qrcode_image(qr_str_data):
    """
    根据字符串生成默认的二维码
    :param qr_str_data:
    :return: type:PIL 图片
    """
    qr = qrcode.QRCode(
            version=8,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=1,
        )
    qr.add_data(qr_str_data)
    qr.make(fit=True)

    img = qr.make_image()

    return img
