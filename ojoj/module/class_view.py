from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from rest_framework import generics
from rest_framework.response import Response
from ..models import Class, School, Users
from ..serializers import ClassSerializer, StudentSerializer
from ..utils import data_wrapper, get_params_from_post
from .core import BaseListView


class ClassView(BaseListView):
    queryset = Class.objects.all().order_by('-grade')
    serializer_class = ClassSerializer

    def get_dataset(self, request):
        academy_id = request.GET.get('academy_id', None)
        grade = request.GET.get('grade', None)
        dataset = self.get_queryset()

        try:
            if academy_id:
                academy = School.objects.get(id=academy_id)
                dataset = dataset.filter(academy_id=academy)
            if grade:
                dataset = dataset.filter(grade=grade)
        except:
            return dataset.none()
        return dataset

    def post(self, request):
        namedict = {'class_id': 20001, 'class_name': 20001, 'grade': 20001, 'academy_id': 20001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            return Response(data_wrapper(success="false", msg=params['error']))
        if self.queryset.filter(class_id=params['class_id']).exists():
            return Response(data_wrapper(success="false", msg=30000))
        try:
            academy_id = School.objects.get(id=params['academy_id'])
            new_cls = Class.objects.create(class_id=params['class_id'], class_name=params['class_name'],
                             grade=params['grade'], academy_id=academy_id, studentnum=0)
            new_cls.save()
            return Response(data_wrapper(success="true", msg=30002, data=self.get_serializer(new_cls).data))
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=30001))



class ClassDetailView(generics.GenericAPIView):

    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def get(self, request):
        page = request.GET.get('page', 1)
        pagesize = request.GET.get('pagesize', 10)
        try:
            class_id = request.GET['class_id']
            class_obj = self.queryset.get(pk=class_id)
            dataset = class_obj.users_set.all().order_by('code')
            paginaor = Paginator(dataset, pagesize)
            students = paginaor.get_page(page)
        except KeyError:
            return Response(data_wrapper(success="false", msg=20001))
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except PageNotAnInteger:
            students = paginaor.get_page(1)
        except EmptyPage:
            students = paginaor.get_page(paginaor.count)
        cls_serializer = self.get_serializer(class_obj)
        stu_serializer = StudentSerializer(students, many=True)
        data = {
            'info': cls_serializer.data,
            'students': stu_serializer.data
        }
        return Response(data_wrapper(data, success="true"))

    def put(self, request):
        """
        为班级添加学生
        :param request:
        :return:
        """
        namedict = {'class_id': 20001, 'code': 20001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            return Response(data_wrapper(success="false", msg=params['error']))
        try:
            student = Users.objects.get(code=params['code'])
            cls = Class.objects.get(class_id=params['class_id'])
            student.class_id = cls
            student.save()
            cls.studentnum = cls.users_set.all().count()
            cls.save()
            return Response(data_wrapper(success="true", data=self.get_serializer(cls).data))
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false"))