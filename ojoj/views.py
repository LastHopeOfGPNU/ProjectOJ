from django.http import HttpResponse
from .utils import ValidateCode
from .models import Loginlog
from django.utils import timezone
from django.shortcuts import render
import os

def index(request):
    return render(request, 'ojoj/index.html')

def captcha(request):
    vc = ValidateCode()
    img = vc.gen_img()
    code = vc.get_code()
    img.save(open("ojoj/tmp/%s.png" % code, "wb"), format="png")

    Loginlog.objects.create(captcha=code, ip=request.META['REMOTE_ADDR'], time=timezone.now()).save()
    img = open("ojoj/tmp/%s.png" % code, "rb").read()
    os.remove("ojoj/tmp/%s.png" % code)
    return HttpResponse(img, content_type="image/png")


