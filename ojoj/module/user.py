from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from ..models import Users
from ..serializers import UserSerializer
from ..utils import pwCheck
from hashlib import md5
from ..meta.msg import MSG_DICT
from time import time
from ..utils import get_params_from_post

# TODO: 写注释，检查参数
class UserRegisterView(APIView):
    def post(self, request):
        ip = request.META['REMOTE_ADDR']
        namedict = {'username': 10000, 'nickname': 10006, 'password': 10001, 'captchacode': 10005}
        params = get_params_from_post(request, namedict)

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

class UserLoginView(generics.GenericAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        # 检查参数
        success = 'false'
        msg = 10002
        namedict = {'username': 10000, 'password': 10001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            msg = params['error']
        md5_ins = md5()
        if msg == 10002:
            try:
                user = self.queryset.get(user_id=params['username'])
                if pwCheck(params['password'], user.password):
                    if user.defunct == 'Y':
                        msg = 10013
                    # 设置用户cookie
                    md5_ins.update(str(time()).encode() + params['username'].encode())
                    cookie = md5_ins.hexdigest()
                    ip = request.META['REMOTE_ADDR']
                    # 更新用户状态
                    user.cookie = cookie
                    user.ip = ip
                    user.login_time = timezone.now()
                    user.save()
                    success = 'true'
                else:
                    msg = 10003
            except Users.DoesNotExist:
                msg = 10003
        if msg != 10002:
            user = None
        serializer = self.get_serializer(user)
        serializer.set_success(success)
        serializer.set_msg(msg)
        return Response(serializer.data)
