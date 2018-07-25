from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from rest_framework import generics
from rest_framework.response import Response
from ..models import Class, School, Users
from ..serializers import ClassSerializer, StudentSerializer
from ..utils import data_wrapper, get_params_from_post


class ClassView(generics.GenericAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def get(self, request):
        page = request.GET.get('page', 1)
        pagesize = request.GET.get('pagesize', 10)
        dataset = self.get_queryset()
        paginaor = Paginator(dataset, pagesize)
        try:
            classes = paginaor.get_page(page)
        except PageNotAnInteger:
            classes = paginaor.get_page(1)
        except EmptyPage:
            classes = paginaor.get_page(paginaor.count)
        serializer = self.get_serializer(classes, many=True)
        return Response(data_wrapper(serializer.data, success="true"))

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
            return Response(data_wrapper(success="true", msg=30002))
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=30001))

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
            return Response(data_wrapper(success="true"))
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false"))


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

