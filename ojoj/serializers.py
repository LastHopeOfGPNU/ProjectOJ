from rest_framework import serializers
from .models import Users


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('uid', 'user_id', 'nick', 'contact')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('uid', 'user_id', 'nick', 'identity', 'cookie', 'avatarurl')
