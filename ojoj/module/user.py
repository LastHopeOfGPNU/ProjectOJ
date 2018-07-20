from django.utils import timezone
from django.core.validators import validate_email, ValidationError
from django.db.utils import OperationalError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from ..models import Users
from ..models import Loginlog
from ..serializers import UserSerializer,TeacherSerializer
from ..utils import pwCheck, pwGen
from hashlib import md5
from time import time
from ..utils import get_params_from_post
from ..meta.msg import MSG_DICT

def data_wrapper(data="", msg="", success=""):
    msg = MSG_DICT.get(msg, "")
    return {'success': success, 'msg': msg, 'data': data}

class TeacherView(generics.GenericAPIView):
    queryset = Users.objects.filter(identity=2)
    serializer_class = TeacherSerializer
    def get(self, request):
        serializer = self.get_serializer(self.queryset.all(), many=True)
        return Response(data_wrapper(serializer.data, success="true"))


class UserRegisterView(APIView):
    def post(self, request):
        success = "true"
        msg = 10007
        ip = request.META['REMOTE_ADDR']
        namedict = {'username': 10000, 'nickname': 10006, 'password': 10001, 'captchacode': 10005}
        params = get_params_from_post(request, namedict)
        try:
            if params['error']:
                raise KeyError

        # 从loginlog表中查询验证码是否正确
        # select count(*) from loginlog where ip=xxx and captcha=xxx
            loginlog = Loginlog.objects.get(ip=ip, captcha=params['captchacode'])
            loginlog.delete()

        # 限制登录账号为电子邮箱（检查user_id）
            validate_email(params['username'])

        # 检查用户是否存在
            user = Users.objects.get(user_id=params['username'])
            raise ValueError
        except Loginlog.DoesNotExist:
            msg = 10005
        except KeyError:
            msg = params['error']
        except ValidationError:
            msg = 10000
        except ValueError:
            msg = 10008
        except Users.DoesNotExist:
            # 加密密码
            password = pwGen(params['password'])
            # 数据库中插入新用户
            try:
                # INSERT INTO `users`(`user_id`,`email`,`ip`,`accesstime`,`password`,`reg_time`,`nick`)
                # 成功返回10007，失败返回10009
                Users.objects.create(user_id=params['username'], email=params['username'], ip=ip, accesstime=timezone.now(),
                                 password=password, reg_time=timezone.now(), nick=params['nickname']).save()
            except OperationalError:
                msg = 10009
            else:
                msg = 10007
        if msg != 10007:
            success = "false"
        return Response(data_wrapper(msg=msg, success=success))

# TODO: 重构？
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
        return Response(data_wrapper(msg=msg, success=success, data=serializer.data))
