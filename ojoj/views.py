from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Users
from.serializers import UserSerializer



def index(request):
    return HttpResponse("Hi, index.")

# 标记可被跨站访问
@csrf_exempt
def users(request):
    if request.method == 'GET':
        user = Users.objects.get(user_id='2015034743003')
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)

