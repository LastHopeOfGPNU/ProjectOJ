from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from .models import Users
from .serializers import UserSerializer, BaseSerializer
from .utils import pwCheck
from hashlib import md5
from .meta.msg import MSG_DICT
from time import time

def index(request):
    return HttpResponse("Hi, index.")

# TODO: 写注释，检查参数
class UserRegisterView(APIView):
    def post(self, request):
        user_id = request.POST['username']
        nick = request.POST['nickname']
        password = request.POST['password']
        captchacode = request.POST['captchacode']  # 或返回10005
        ip = request.META['REMOTE_ADDR']

        # TODO: 从loginlog表中查询验证码是否正确
        # select count(*) from loginlog where ip=xxx and captcha=xxx
        # 不正确返回10005
        # 正确：delete from loginlog where ip=xxx and captcha=xxx

        # TODO：限制登录账号为电子邮箱（检查user_id）

        # TODO：检查用户是否存在

        # TODO：加密密码

        # TODO: 数据库中插入新用户
        # INSERT INTO `users`(`user_id`,`email`,`ip`,`accesstime`,`password`,`reg_time`,`nick`)
        # 成功返回10007，失败返回10009

class UserLoginView(APIView):

    def post(self, request):
        # TODO: 需要检查参数
        success = 'false'
        user_id = request.POST['username']
        password = request.POST['password']
        msg = 10002
        md5_ins = md5()
        try:
            user = Users.objects.get(user_id=user_id)
            # serializer = UserSerializer(user)
            base = BaseSerializer()
            if pwCheck(password, user.password):
                if user.defunct == 'Y':
                    msg = 10013
                md5_ins.update(str(time()).encode() + user_id.encode())
                cookie = md5_ins.hexdigest()
                ip = request.META['REMOTE_ADDR']
                user.cookie = cookie
                user.ip = ip
                user.login_time = timezone.now()
                user.save()
                base.set_serializer(UserSerializer(user))
                success = 'true'
            else:
                msg = 10003
        except Users.DoesNotExist:
            msg = 10003
        return Response(base.render(success, MSG_DICT[msg]))
#class UserView(generics.RetrieveAPIView):
#    queryset = Users.objects.all()
#    serializer_class = UserSerializer
#    lookup_field = 'user_id'

