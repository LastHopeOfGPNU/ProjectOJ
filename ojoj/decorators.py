from rest_framework.response import Response
from .utils import data_wrapper
from .models import Users


def login_required(func):
    def wrapper(cls, request):
        try:
            cookie = request.GET['cookie']
            user = Users.objects.get(cookie=cookie)
            request.session['identity'] = str(user.identity)
            return func(cls, request)
        except Exception as e:
            print(e)
            return Response(data_wrapper(msg=10011, success="false"))
    return wrapper

# define identities
ID_GUEST = -1
ID_REGULAR = 0
ID_STUDENT = 1
ID_TEACHER = 2
ID_ADMIN = 3


def identity_required(identity):
    def decorator(func):
        def wrapper(cls, request):
            u_identity = int(request.session.get('identity', ID_GUEST))
            if u_identity < identity:
                return Response(data_wrapper(msg=20003, success="false"))
            else:
                return func(cls, request)
        return wrapper
    return decorator
