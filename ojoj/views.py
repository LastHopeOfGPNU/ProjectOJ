from django.http import HttpResponse

def index(request):
    return HttpResponse("Hi, index.")

#class UserView(generics.RetrieveAPIView):
#    queryset = Users.objects.all()
#    serializer_class = UserSerializer
#    lookup_field = 'user_id'

