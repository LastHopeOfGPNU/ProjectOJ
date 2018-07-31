from rest_framework import serializers
from .models import Users, Class, School, CoursesTeacher


class TeacherSerializer(serializers.ModelSerializer):
    academy_name = serializers.SerializerMethodField()
    major_name = serializers.SerializerMethodField()
    course_num = serializers.SerializerMethodField()

    def get_academy_name(self, obj):
        return obj.academy.name

    def get_major_name(self, obj):
        try:
            return School.objects.get(pk=obj.major).name
        except:
            return ""

    def get_course_num(self, obj):
        return CoursesTeacher.objects.filter(teacher_id=obj.uid).count()

    class Meta:
        model = Users
        fields = ('uid', 'user_id', 'nick', 'contact', 'code', 'academy_name', 'major_name', 'course_num')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('uid', 'user_id', 'nick', 'identity', 'cookie', 'avatarurl', 'reg_time', 'login_time',
                  'email', 'sex', 'qq', 'signature')


class StudentSerializer(serializers.ModelSerializer):
    academy_name = serializers.SerializerMethodField()
    class_name = serializers.SerializerMethodField()

    def get_academy_name(self, obj):
        try:
            return obj.academy.name
        except:
            return ""

    def get_class_name(self, obj):
        try:
            return obj.class_id.class_name
        except:
            return ""

    class Meta:
        model = Users
        fields = ('uid', 'code', 'nick', 'sex', 'submit', 'solved', 'login_time', 'academy_name', 'class_name',
                  'contact')


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

