from rest_framework import serializers
from .models import Users
class BaseSerializer:
    def __init__(self, serializer = None):
        self.serializer = serializer
        self.base = {
            'success': '',
            'msg': '',
            'data': {}
        }

    def set_serializer(self, serializer):
        self.serializer = serializer

    def set_data_content(self, key, value):
        self.base['data'][key] = value

    def render(self, success, msg):
        self.base['success'] = success
        self.base['msg'] = msg
        self.base['data'] = '' if not self.serializer else self.serializer.data
        return self.base

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('uid', 'user_id', 'nick', 'identity', 'cookie', 'avatarurl')
