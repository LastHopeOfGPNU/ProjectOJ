from django.utils import timezone
from django.core.validators import validate_email, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import OperationalError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from ..models import Users, School
from ..models import Loginlog
from ..serializers import UserSerializer,TeacherSerializer
from ..utils import pwCheck, pwGen
from hashlib import md5
from time import time
from ..utils import get_params_from_post, data_wrapper
from ..decorators import login_required, identity_required, ID_ADMIN


class TeacherView(generics.GenericAPIView):
    queryset = Users.objects.all()
    serializer_class = TeacherSerializer
    def get(self, request):
        page = request.GET.get('page', 1)
        pagesize = request.GET.get('pagesize', 10)
        dataset = self.queryset.filter(identity=2).order_by('uid')
        paginaor = Paginator(dataset, pagesize)
        try:
            teachers = paginaor.get_page(page)
        except PageNotAnInteger:
            teachers = paginaor.get_page(1)
        except EmptyPage:
            teachers = paginaor.get_page(paginaor.count)
        serializer = self.get_serializer(teachers, many=True)
        return Response(data_wrapper(serializer.data, success="true"))

    def post(self, request):
        namedict = {'code': 20001, 'nick': 20001, 'sex': 20001, 'academy': 20001, 'major': 20001,
                    'contact': 20001, 'email': 20001, 'qq': 20001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            return Response(data_wrapper(msg=params['error'], success="false"))

        # 检查user_id是否存在
        user = self.queryset.filter(user_id=params['code'])
        try:
            academy = School.objects.get(pk=params['academy'])
            # 存在的话就做他老师
            if user.count() != 0:
                user = user[0]
                user.identity = 2
                user.academy = academy
                user.major = params['major']
                user.save()
            # 不存在就做他存在
            else:
                password = pwGen("123456")
                ip = request.META['REMOTE_ADDR']

                # create & insert
                user = Users.objects.create(user_id=params['code'], code=params['code'], nick=params['nick'], sex=params['sex'],
                                            academy=academy, major=params['major'],
                                            contact=params['contact'], email=params['email'], qq=params['qq'],
                                            password=password, ip=ip, identity=2) # identity=2代表老师身份
                user.save()
        except OperationalError:
            return Response(data_wrapper(msg=20001, success="false"))
        except ObjectDoesNotExist:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(success="true", data=self.get_serializer(user).data))

    def delete(self, request):
        # 通过uid删除老师
        namedict = {'uid': 20001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            return Response(data_wrapper(msg=params['error'], success="false"))
        user = self.queryset.filter(identity=2, uid=params['uid'])
        if user.count() != 0:
            # 只是将身份重置为0（默认普通用户），并非真正删除
            user = user[0]
            user.identity = 0
            user.save()
        return Response(data_wrapper(success="true"))

    def put(self, request):
        namedict = {'code': 20001, 'nick': 20001, 'sex': 20001, 'academy': 20001, 'major': 20001,
                    'contact': 20001, 'email': 20001, 'qq': 20001, 'uid': 20001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            return Response(data_wrapper(msg=params['error'], success="false"))
        try:
            user = self.queryset.get(uid=params['uid'])
            for key, value in params.items():
                if key == 'academy':
                    user.academy = School.objects.get(pk=params['academy'])
                else:
                    setattr(user, key, value)
            user.save()
            serializer = self.get_serializer(user)
        except ObjectDoesNotExist:
            return Response(data_wrapper(msg=20001, success="false"))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(data=serializer.data, success="true"))


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


class UserView(generics.GenericAPIView):
    queryset = Users.objects.all().order_by('-uid')
    serializer_class = UserSerializer

    @login_required
    @identity_required(ID_ADMIN)
    def get(self, request):
        page = request.GET.get('page', 1)
        pagesize = request.GET.get('pagesize', 10)
        dataset = self.get_queryset()
        paginaor = Paginator(dataset, pagesize)
        try:
            users = paginaor.get_page(page)
        except PageNotAnInteger:
            users = paginaor.get_page(1)
        except EmptyPage:
            users = paginaor.get_page(paginaor.count)
        serializer = self.get_serializer(users, many=True)
        return Response(data_wrapper(serializer.data, success="true"))

    @login_required
    @identity_required(ID_ADMIN)
    def put(self, request):
        namedict = {'uid': 20001, 'nick': 20001, 'email': 20001, 'sex': 20001, 'qq': 20001, 'signature': 20001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            return Response(data_wrapper(success="false", msg=params['error']))
        try:
            user = self.queryset.get(pk=params['uid'])
            for key, value in params.items():
                setattr(user, key, value)
            user.save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(data=self.get_serializer(user).data, success="true"))