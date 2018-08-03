from django.urls import path
from . import views
from .module.user import *
from .module.class_view import *
from .module.student import *
from .module.school import *
from .module.problem import *
from django.conf.urls import url

app_name = 'ojoj'
urlpatterns = [
    # API URL
    path('captcha', views.captcha, name='captcha'),
    url('users/login/$', UserLoginView.as_view()),
    url('users/register/$', UserRegisterView.as_view()),
    url('users$', UserView.as_view()),
    url('users/teachers', TeacherView.as_view()),
    url('classes$', ClassView.as_view()),
    url('classes/detail', ClassDetailView.as_view()),
    url('students$', StudentView.as_view()),
    url('students/detail', StudentDetailView.as_view()),
    url('schools$', SchoolView.as_view()),
    url('problems$', ProblemView.as_view()),
    url('problems/detail', ProblemDetailView.as_view()),
    # 页面URL
    path('', views.index, name='index'),
]