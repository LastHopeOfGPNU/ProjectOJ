import base64
from hashlib import md5, sha1
from random import random, randint
from io import StringIO
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db import connection
from .meta.msg import MSG_DICT
from .models import Problem

encoding = 'utf-8'

def execute_raw_sql(sql):
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
    except:
        pass
    return cursor.fetchall()

def set_accept_rate():
    problems = Problem.objects.all()
    for problem in problems:
        try:
            problem.accept_rate = problem.accepted / problem.submit
            problem.save()
        except:
            continue
    print('OK')

def get_pagination_data(request, get_serializer, queryset):
    page = request.GET.get('page', 1)
    pagesize = request.GET.get('pagesize', 10)
    paginaor = Paginator(queryset, pagesize)
    try:
        users = paginaor.get_page(page)
    except PageNotAnInteger:
        users = paginaor.get_page(1)
    except EmptyPage:
        users = paginaor.get_page(paginaor.count)
    serializer = get_serializer(users, many=True)
    return {
        "data": serializer.data,
        "total": queryset.count()
    }


def data_wrapper(data="", msg=0, success=""):
    msg = MSG_DICT.get(msg, "")
    return {'success': success, 'msg': msg, 'data': data}

def get_params_from_post(request, namedict):
    """
    传入request和需要获得的POST参数名字典namedict
    返回dict，错误信息在error域中
    :param request:
    :param namedict: key：参数名，value：错误代码
    :return:
    """
    ret = {'error': None}
    for param in namedict.keys():
        try:
            value = request.POST[param]
            ret[param] = value
        except KeyError:
            ret['error'] = namedict[param]
            continue
    return ret

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

class ValidateCode:
    """
    验证码类
    """
    def __init__(self):
        self.__charset = "abcdefghkmnprstuvwxyzABCDEFGHKMNPRSTUVWXYZ23456789"
        self.__setlen = len(self.__charset) - 1
        self.__codelen = 4
        self.__fontsize = 35
        self.__imgsize = (130, 50)
        self.__bgcolor = (255, 255, 255)
        self.__fontcolor = (0, 0, 0)
        self.__code = ""

    def create_code(self):
        code = StringIO()
        for i in range(self.__codelen):
            offset = randint(0, self.__setlen)
            code.write(self.__charset[offset])
        return code.getvalue()

    def gen_img(self):
        img = Image.new("RGB", self.__imgsize, self.__bgcolor)
        font = ImageFont.truetype("ojoj/font/elephant.ttf", self.__fontsize)
        draw = ImageDraw.Draw(img)  # 创建画笔
        self.__code = self.create_code()
        font_width, font_height = font.getsize(self.__code)
        # 放字
        x = (self.__imgsize[0] - font_width) / self.__codelen
        y = (self.__imgsize[1] - font_height) / self.__codelen
        draw.text((x, y), self.__code, font=font, fill=self.__fontcolor)
        # 扭曲图片
        img = img.transform((self.__imgsize[0], self.__imgsize[1]), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

        return img

    def get_code(self):
        return self.__code.lower()

