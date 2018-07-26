from django.urls import path
from . import views
from .module.user import *
from .module.class_view import *
from .module.student import *
from django.conf.urls import url

app_name = 'ojoj'
urlpatterns = [
    path('', views.index, name='index'),
    path('captcha', views.captcha, name='captcha'),
    url('users/login/$', UserLoginView.as_view()),
    url('users/register/$', UserRegisterView.as_view()),
    url('users/teachers', TeacherView.as_view()),
    url('classes$', ClassView.as_view()),
    url('classes/detail', ClassDetailView.as_view()),
    url('students$', StudentView.as_view()),
    url('students/detail', StudentDetailView.as_view())
]