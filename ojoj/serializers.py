from rest_framework import serializers
from .models import Users, Class


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('uid', 'user_id', 'nick', 'contact')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('uid', 'user_id', 'nick', 'identity', 'cookie', 'avatarurl')


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('uid', 'code', 'nick', 'sex', 'submit', 'solved', 'login_time')


class ClassSerializer(serializers.ModelSerializer):
    course_num = serializers.SerializerMethodField()
    academy_name = serializers.SerializerMethodField()

    def get_academy_name(self, obj):
        return obj.academy_id.name

    def get_course_num(self, obj):
        return obj.courses.all().count()

    class Meta:
        model = Class
        fields = ('class_id', 'class_name', 'grade', 'studentnum', 'course_num', 'academy_name')

