"""
rsa的编码和解码,
参考资料:http://blog.csdn.net/u013166622/article/details/50959421

和数据库相关的配置,用rsa,其它的可以用明文
"""

import base64
import rsa


def gen_rsa_key_pair_file(file_name, base_path='.', key_len=512):
    """
    生成一对RSA的文件对
    :return:
    """
    import os
    pub_file = os.path.join(base_path, '%s.pub' % file_name)
    pri_file = os.path.join(base_path, file_name)

    (pub_key, pri_key) = rsa.newkeys(key_len)

    pub = pub_key.save_pkcs1()
    pub_key_file = open(pub_file, 'w+')
    pub_key_file.write(pub.decode('utf-8'))
    pub_key_file.close()

    pri = pri_key.save_pkcs1()
    pri_key_file = open(pri_file, 'w+')
    # pri_key_file.write(bytes.decode(pri))
    pri_key_file.write(pri.decode('utf-8'))
    pri_key_file.close()


def get_encrypt_str(public_key_file, raw_msg):
    """
    对原始数据进行RSA加密,每次运行的结果不一样
    :return:
    """

    publickfile = open(public_key_file)
    p = publickfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)

    # 用公钥加密、再用私钥解密
    crypto = rsa.encrypt(str.encode(raw_msg), pubkey)  # 使用公钥对信息加密
    base64str_crypto = bytes.decode(base64.b64encode(crypto))  # 密文byte串转base64串
    return base64str_crypto


def get_decrypt_str(private_key_file, encrypt_msg):
    """
    使用私钥进行解密，将密文变成原始文
    :param private_key_file:
    :param encrypt_msg:
    :return:
    """
    key_file = open(private_key_file)
    p = key_file.read()
    key = rsa.PrivateKey.load_pkcs1(p)

    # 用私钥解密
    decode_crypto = base64.b64decode(str.encode(encrypt_msg))  # base64串转密文byte
    decode_message = rsa.decrypt(decode_crypto, key)  # 使用私钥对信息还原
    decode_message_str = bytes.decode(decode_message)
    return decode_message_str


def demo_rsa_code():
    """
    演示整个RSA的加密解密过程
    :return:
    """
    pri_kfile = 'config_rsa'
    pub_kfile = 'config_rsa.pub'

    raw_msg = 'my-password'

    secret_msg = get_encrypt_str(pub_kfile, raw_msg)
    print(secret_msg)

    decode_msg = get_decrypt_str(pri_kfile, secret_msg)
    print(decode_msg)


if __name__ == '__main__':
    # gen_rsa_key_pair()
    # gen_rsa_key_pair_file('new_rsa')
    # rsa_keys_demo()
    demo_rsa_code()
    pass
