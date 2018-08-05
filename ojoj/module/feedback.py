from rest_framework.response import Response
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from .core import BaseListView
from ..models import Feedback, Users
from ..serializers import FeedbackSerializer
from ..utils import get_params_from_post, data_wrapper

class FeedbackView(BaseListView):
    queryset = Feedback.objects.all().order_by('-fid')
    serializer_class = FeedbackSerializer
    pk_field = 'fid'

    def get_dataset(self, request):
        try:
            fid = request.GET['fid']
            return self.get_queryset().filter(fid=fid)
        except:
            return self.get_queryset()

    def post(self, request):
        namedict = {'uid': 20001, 'title': 20001, 'content': 20001, 'type': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(success="false", msg=20001))
        try:
            params['uid'] = Users.objects.get(uid=params['uid'])
            fb = Feedback.objects.create(**params)
            fb.save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(success="true", data=self.get_serializer(fb).data))

    def put(self, request):
        namedict = {'fid': 20001, 'is_mark': 20001, 'is_solved': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(success="false", msg=20001))
        try:
            fb = self.get_queryset().get(pk=params.pop('fid'))
            for key, value in params.items():
                setattr(fb, key, value)
            fb.save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(success="true", data=self.get_serializer(fb).data))