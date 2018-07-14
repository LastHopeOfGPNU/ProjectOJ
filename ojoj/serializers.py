from rest_framework import serializers
from .models import Users
class BaseSerializer:
    def __init__(self, serializer):
        self.serializer = serializer
        self.base = {
            'success': '',
            'msg': '',
            'data': ''
        }

    def render(self, success, msg):
        self.base['success'] = success
        self.base['msg'] = msg
        self.base['data'] = self.serializer.data
        return self.base

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('user_id', 'nick')
