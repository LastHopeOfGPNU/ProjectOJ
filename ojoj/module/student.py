from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
import xlrd
import re
import os
from xlrd.biffh import XLRDError
from ..utils import data_wrapper, pwGen, get_params_from_post
from ..serializers import StudentSerializer
from ..models import Users, School, Class
from .core import BaseListView


def create_student(params):
    # 检查user_id是否存在
    user = Users.objects.filter(user_id=params['code'])
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
        ip = params['ip']
        # create & insert
        user = Users.objects.create(user_id=params['code'], code=params['code'], nick=params['nick'], sex=params['sex'],
                                    academy=academy, grade=params['grade'], class_id=class_id,
                                    password=password, ip=ip, identity=1) # identity=1代表学生身份

        user.save()
        class_id.studentnum = class_id.users_set.all().count()
        class_id.save()
    return user

class StudentFileView(generics.GenericAPIView):

    def post(self, request):
        try:
            data = request.FILES['file']
            filename = str(timezone.now())
            filename = "%s.xlsx" % re.sub(r'\D', '', filename) # 只留下数字
            path = 'ojoj/tmp/%s' % filename
            # 临时存放上传文件
            with open(path, 'wb') as file:
                for i in data: file.write(i)
            total = 0
            workbook = xlrd.open_workbook(path)
            sheet = workbook.sheet_by_index(0)
            # 开始迭代每一行
            for i in range(1, sheet.nrows):
                row = sheet.row_values(i)
                # 填充学生的每个字段
                # 'code': 20001, 'nick': 20001, 'sex': 20001, 'academy': 20001, 'grade': 20001,
                #    'class_id': 20001
                params = {
                    'code': str(int(row[0])), 'nick': row[1], 'sex': int(row[2]), 'academy': int(row[3]),
                    'grade': int(row[4]), 'class_id': int(row[5]),
                    'ip': request.META['REMOTE_ADDR']
                }
                student = create_student(params)
                total += 1
        except KeyError:
            return Response(data_wrapper(msg=20001, success="false"))
        except XLRDError:
            return Response({'data': '', 'msg': '文件格式不支持', 'success': 'false'})
        except Exception as e:
            print(e)
            msg = '表格格式有误，已添加学生%d名，请检查第%d行数据' % (total, total+2)
            return Response({'data': '', 'msg': msg, 'success': 'false'})
        finally:
            # 删除临时文件
            os.remove(path)
        return Response({'msg': '成功添加学生%d名' % total, 'success': 'true', 'data': ''})


class StudentView(BaseListView):
    queryset = Users.objects.filter(identity=1).order_by('-uid')
    serializer_class = StudentSerializer

    def post(self, request):
        namedict = {'code': 20001, 'nick': 20001, 'sex': 20001, 'academy': 20001, 'grade': 20001,
                    'class_id': 20001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            return Response(data_wrapper(msg=params['error'], success="false"))
        try:
            params['ip'] = request.META['REMOTE_ADDR']
            user = create_student(params)
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
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
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
