from rest_framework import generics
from rest_framework.response import Response
from ..models import School
from ..utils import data_wrapper


class SchoolView(generics.GenericAPIView):
    queryset = School.objects.all()

    def get(self, request):
        academy_id = request.GET.get('academy_id', 0)
        majors = self.queryset.filter(academy_id=academy_id)
        major_list = [major.name for major in majors]
        return Response(data_wrapper(data=major_list, success="true"))