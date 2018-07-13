from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from .models import Users
from .serializers import UserSerializer


def index(request):
    return HttpResponse("Hi, index.")

#class UserView(APIView):

#    def get(self, request, user_id):
#        user = get_object_or_404(Users, user_id=user_id)
#        serializer = UserSerializer(user)
#        return Response(serializer.data)
class UserView(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'

