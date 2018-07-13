from django.test import TestCase
import base64
from hashlib import md5, sha1

save = 'cFoqYj1KzV7nTlv0fGckWZ9y8XRmYzg0'
def pwCheck(password, saved):
    svd = base64.b64decode(saved.encode('ascii'))
    salt = svd[20:]

    md5_ins = md5()
    sha1_ins = sha1()

    md5_ins.update(password.encode('ascii'))
    md5_out = md5_ins.digest() + salt

    sha1_ins.update(md5_out)
    sha1_out = sha1_ins.digest() + salt
    final_out = base64.b64encode(sha1_out).decode('ascii')
    return final_out

print(pwCheck('a28721054', save))