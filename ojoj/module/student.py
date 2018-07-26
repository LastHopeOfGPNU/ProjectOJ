from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from rest_framework import generics
from rest_framework.response import Response
from ..utils import data_wrapper, pwGen, get_params_from_post
from ..serializers import StudentSerializer
from ..models import Users, School, Class

class StudentView(generics.GenericAPIView):
    queryset = Users.objects.filter(identity=1)
    serializer_class = StudentSerializer
    def get(self, request):
        page = request.GET.get('page', 1)
        pagesize = request.GET.get('pagesize', 10)
        dataset = self.get_queryset()
        paginaor = Paginator(dataset, pagesize)
        try:
            students = paginaor.get_page(page)
        except PageNotAnInteger:
            students = paginaor.get_page(1)
        except EmptyPage:
            students = paginaor.get_page(paginaor.count)
        serializer = self.get_serializer(students, many=True)
        return Response(data_wrapper(serializer.data, success="true"))

    def post(self, request):
        namedict = {'code': 20001, 'nick': 20001, 'sex': 20001, 'academy': 20001, 'grade': 20001,
                    'class_id': 20001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            return Response(data_wrapper(msg=params['error'], success="false"))

        # 检查user_id是否存在
        user = Users.objects.filter(user_id=params['code'])
        try:
            academy = School.objects.get(pk=params['academy'])
            class_id = Class.objects.get(pk=params['class_id'])
            # 存在的话就做他学生
            if user.count() != 0:
                user = user[0]
                user.identity = 1
                user.academy = academy
                user.class_id = class_id
                class_id.studentnum = class_id.users_set.all().count()
                class_id.save()
                user.save()
            # 不存在就做他存在
            else:
                password = pwGen("123456")
                ip = request.META['REMOTE_ADDR']
                # create & insert
                user = Users.objects.create(user_id=params['code'], code=params['code'], nick=params['nick'], sex=params['sex'],
                                            academy=academy, grade=params['grade'], class_id=class_id,
                                            password=password, ip=ip, identity=2) # identity=1代表学生身份

                user.save()
                class_id.studentnum = class_id.users_set.all().count()
                class_id.save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(msg=20001, success="false"))
        except OperationalError:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(success="true", data=self.get_serializer(user).data))

    def delete(self, request):
        namedict = {'uid': 20001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            return Response(data_wrapper(msg=params['error'], success="false"))
        user = self.queryset.filter(identity=1, uid=params['uid'])
        if user.count() != 0:
            # 只是将身份重置为0（默认普通用户），并非真正删除
            user = user[0]
            cls = user.class_id
            user.identity = 0
            user.class_id = None
            user.save()
            cls.studentnum = cls.users_set.all().count()
            cls.save()
        return Response(data_wrapper(success="true"))

    def put(self, request):
        namedict = {'uid': 20001, 'code': 20001, 'nick': 20001, 'sex': 20001, 'academy': 20001, 'grade': 20001,
                    'class_id': 20001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            return Response(data_wrapper(success="false", msg=params['error']))
        try:
            student = self.queryset.get(pk=params['uid'])
            for key, value in params.items():
                if key == 'academy':
                    student.academy = School.objects.get(pk=params['academy'])
                elif key == 'class_id':
                    student.class_id = Class.objects.get(pk=params['class_id'])
                else:
                    setattr(student, key, value)
            student.save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=params['error']))
        return Response(data_wrapper(data=self.get_serializer(student).data, success="true"))




class StudentDetailView(generics.GenericAPIView):
    queryset = Users.objects.filter(identity=1)
    serializer_class = StudentSerializer

    def get(self, request):
        try:
            code = request.GET['code']
            student = self.queryset.get(code=code)
        except KeyError:
            return Response(data_wrapper(msg=20001, success="false"))
        except ObjectDoesNotExist:
            return Response(data_wrapper(msg=20001, success="false"))
        else:
            return Response(data_wrapper(data=self.get_serializer(student).data, success="true"))
