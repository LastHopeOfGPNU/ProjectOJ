from rest_framework.response import Response
from .core import BaseListView
from ..models import AboutUs
from ..serializers import AboutUsSerializer
from ..utils import get_params_from_post, data_wrapper


class AboutUsView(BaseListView):
    queryset = AboutUs.objects.all().order_by('grade')
    serializer_class = AboutUsSerializer
    pk_field = 'id'

    def post(self, request):
        namedict = {'name': 20001, 'avatarurl': 20001, 'description': 20001, 'job': 20001, 'grade': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            about_us = AboutUs.objects.create(**params)
            about_us.save()
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(data=self.get_serializer(about_us).data, success="true"))

    def put(self, request):
        namedict = {'id': 20001, 'name': 20001, 'avatarurl': 20001, 'description': 20001, 'job': 20001, 'grade': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            about_us = AboutUs.objects.get(id=params.pop('id'))
            for key, value in params.items():
                setattr(about_us, key, value)
            about_us.save()
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(data=self.get_serializer(about_us).data, success="true"))