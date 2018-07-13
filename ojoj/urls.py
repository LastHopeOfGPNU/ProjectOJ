from django.urls import path, include
from . import views

app_name = 'ojoj'
urlpatterns = [
    path('', views.index, name='index'),
]