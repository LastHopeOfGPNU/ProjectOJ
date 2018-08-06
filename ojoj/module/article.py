from rest_framework.response import Response
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from .core import BaseListView
from ..utils import data_wrapper
from ..models import Label, Article
from ..serializers import LabelSerilizer, ArticleSerializer


class ArticleView(BaseListView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_dataset(self, request):
        try:
            labelid = request.GET['labelid']
            label = Label.objects.get(labelid=labelid)
            return label.articles.order_by('-articleid')
        except KeyError:
            return self.queryset.none()
        except ObjectDoesNotExist:
            return self.queryset.none()


class LabelView(BaseListView):
    queryset = Label.objects.all()
    serializer_class = LabelSerilizer

    def get_dataset(self, request):
        try:
            pid = request.GET['pid']
            return self.queryset.filter(pid=pid).order_by('labelid')
        except KeyError:
            return self.queryset.none()
        except ValueError:
            return self.queryset.none()