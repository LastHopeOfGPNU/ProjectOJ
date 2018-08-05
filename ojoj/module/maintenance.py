from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.db import OperationalError
import datetime
from ..utils import data_wrapper, get_params_from_post
from ..models import Maintenance
from ..serializers import MaintenanceSerializer

class MaintenanceView(GenericAPIView):
    queryset = Maintenance.objects.all().order_by('-id')
    serializer_class = MaintenanceSerializer

    def get(self, request):
        return Response(data_wrapper(success="true", data=self.get_serializer(self.get_queryset()[0]).data))

    def post(self, request):
        namedict = {'start': 20001, 'end': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(success="false", msg=20001))
        try:
            params['start'] = datetime.datetime.strptime(params['start'], "%Y-%m-%d %H:%M:%S")
            params['end'] = datetime.datetime.strptime(params['end'], "%Y-%m-%d %H:%M:%S")
            mt = Maintenance.objects.create(**params)
            mt.save()
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(success="true", data=self.get_serializer(mt).data))