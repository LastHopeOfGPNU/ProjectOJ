from rest_framework import generics
from rest_framework.response import Response
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from ..utils import data_wrapper


class BaseListView(generics.GenericAPIView):

    def get_dataset(self, request):
        return self.get_queryset()

    def get(self, request):
        page = request.GET.get('page', 1)
        pagesize = request.GET.get('pagesize', 10)
        dataset = self.get_dataset(request)
        paginaor = Paginator(dataset, pagesize)
        try:
            objs = paginaor.get_page(page)
        except PageNotAnInteger:
            objs = paginaor.get_page(1)
        except EmptyPage:
            objs = paginaor.get_page(paginaor.count)
        serializer = self.get_serializer(objs, many=True)
        data = data_wrapper(success="true")
        data.update({
            'data': serializer.data,
            'total': dataset.count()
        })
        return Response(data)

    def delete(self, request):
        try:
            pk = request.GET[self.pk_field]
            obj = self.get_queryset().get(pk=pk)
            obj.delete()
        except KeyError:
            return Response(data_wrapper(success="false", msg=20001))
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(success="true"))