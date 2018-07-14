from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from .models import Users
from .serializers import UserSerializer, BaseSerializer
from .utils import pwCheck
from hashlib import md5
from .meta.msg import MSG_DICT

def index(request):
    return HttpResponse("Hi, index.")

class UserView(APIView):

    def post(self, request, user_id):
        user_id = request.POST['username']
        password = request.POST['password']
        msg = 10002
        try:
            user = Users.objects.get(user_id=user_id)
            serializer = UserSerializer(user)
            base = BaseSerializer(serializer)
            if pwCheck(password, user.password):
                if user.defunct == 'Y':
                    msg = 10013
        except Users.DoesNotExist:
            msg = 10003
        return Response(base.render("true", MSG_DICT[msg]))
#class UserView(generics.RetrieveAPIView):
#    queryset = Users.objects.all()
#    serializer_class = UserSerializer
#    lookup_field = 'user_id'

