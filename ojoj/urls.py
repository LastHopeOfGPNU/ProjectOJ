from django.urls import path, include
from . import views
from django.conf.urls import url

app_name = 'ojoj'
urlpatterns = [
    path('', views.index, name='index'),
    url('users/login/$', views.UserView.as_view()),
]