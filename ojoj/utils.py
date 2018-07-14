import base64
from hashlib import md5, sha1
from random import random

encoding = 'utf-8'

def hashGen(password, salt):
    """

    :param password: 待hash密码
    :param salt: 加盐(字节串)
    :return: 字符串形式的hash

    digest和hexdigest返回的是完全不同的东西
    digest是原始字节串
    hexdigest是将原始字节串以十六进制编码返回字符串

    Hash过程：password -> md5(password).hexdigest + salt(字符串)
                        -> sha1.digest(这里使用原始字节串) + salt(字节串)
                        ->b64encode
    """
    md5_ins = md5()
    sha1_ins = sha1()

    md5_ins.update(password.encode(encoding))
    hash = md5_ins.hexdigest() + salt.decode(encoding)
    sha1_ins.update(hash.encode(encoding))
    hash = sha1_ins.digest() + salt
    hash = base64.b64encode(hash)

    return hash.decode(encoding)

def pwGen(password):
    sha1_ins = sha1()
    sha1_ins.update(str(random()).encode(encoding))
    salt = sha1_ins.hexdigest()[:4].encode(encoding)  # 只截取前四位
    return hashGen(password, salt)

def pwCheck(password, saved):
    """
    :param password: 待验证的密码
    :param saved: 以保存的密码的Hash
    :return: boolean

    """

    svd = base64.b64decode(saved.encode(encoding))
    salt = svd[20:]
    hash = hashGen(password, salt)
    return hash == saved


