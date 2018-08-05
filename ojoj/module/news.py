from rest_framework.response import Response
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from .core import BaseListView
from ..models import News, Users
from ..serializers import NewsSerializer
from ..utils import get_params_from_post, data_wrapper


class NewsView(BaseListView):
    queryset = News.objects.all().order_by('-time')
    serializer_class = NewsSerializer
    pk_field = 'news_id'

    def post(self, request):
        namedict = {'uid': 20001, 'title': 20001, 'content': 20001,
                    'importance': 20001, 'defunct': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(success="false", msg=20001))
        try:
            params['time'] = timezone.now()
            params['uid'] = Users.objects.get(uid=params['uid'])
            news = News.objects.create(**params)
            news.save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(success="true", data=self.get_serializer(news).data))

    def put(self, request):
        namedict = {'news_id': 20001, 'uid': 20001, 'title': 20001, 'content': 20001,
                    'importance': 20001, 'defunct': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(success="false", msg=20001))
        try:
            news = self.get_queryset().get(news_id=params.pop('news_id'))
            params['uid'] = Users.objects.get(uid=params['uid'])
            params['time'] = timezone.now()
            for key, value in params.items():
                setattr(news, key, value)
            news.save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(success="true", data=self.get_serializer(news).data))


    def get_dataset(self, request):
        try:
            news_id = request.GET['news_id']
            return self.get_queryset().filter(news_id=news_id)
        except:
            return self.get_queryset()