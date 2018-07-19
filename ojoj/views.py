from django.http import HttpResponse
from .utils import ValidateCode
from .models import Loginlog
import datetime
from django.utils import timezone

def index(request):
    return HttpResponse("Hi, index.")

def captcha(request):
    vc = ValidateCode()
    img = vc.gen_img()
    code = vc.get_code()
    img.save(open("ojoj/tmp/%s.png" % code, "wb"), format="png")

    Loginlog.objects.create(captcha=code, ip=request.META['REMOTE_ADDR'], time=timezone.now()).save()
    return HttpResponse(open("ojoj/tmp/%s.png" % code, "rb").read(), content_type="image/png")


