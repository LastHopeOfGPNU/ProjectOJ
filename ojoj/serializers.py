from rest_framework import serializers
from rest_framework.fields import empty
from .models import Users
from .meta.msg import MSG_DICT
class GenericModelSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.base = {
            'success': '',
            'msg': '',
            'data': '',
        }

    @property
    def data(self):
        if self.instance:
            return super().data
        else:
            self.base['data'] = ""
            return self.base

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = ""
        self.base['data'] = data
        return self.base

    def set_success(self, success):
        self.base['success'] = success

    def set_msg(self, code):
        self.base['msg'] = MSG_DICT[code]

class UserSerializer(GenericModelSerializer):

    class Meta:
        model = Users
        fields = ('uid', 'user_id', 'nick', 'identity', 'cookie', 'avatarurl')
