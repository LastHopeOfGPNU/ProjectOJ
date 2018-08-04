from rest_framework import serializers
from .models import *


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


class ProblemSerializer(serializers.ModelSerializer):
    tagnames = serializers.SerializerMethodField()

    def get_tagnames(self, obj):
        return [tag.tagname for tag in obj.tags.all()]

    class Meta:
        model = Problem
        fields = ('problem_id', 'title', 'submit', 'accepted', 'problem_type', 'in_date',
                  'hastestdata', 'tagnames')


class ProblemDetailSerializer(serializers.ModelSerializer):
    tagnames = serializers.SerializerMethodField()
    tagids = serializers.SerializerMethodField()

    def get_tagnames(self, obj):
        return [tag.tagname for tag in obj.tags.all()]

    def get_tagids(self, obj):
        return [tag.tagid for tag in obj.tags.all()]

    class Meta:
        model = Problem
        fields = ('problem_id', 'problem_type', 'title', 'description', 'memory_limit', 'time_limit',
                  'input', 'output', 'sample_output', 'sample_input', 'defunct', 'tagnames', 'tagids',
                  'hint', 'source', 'in_date')


class SolutionSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    error_msg = serializers.SerializerMethodField()

    def get_code(self, obj):
        try:
            return SourceCode.objects.filter(solution_id=obj.solution_id)[0].source
        except:
            return ""

    def get_error_msg(self, obj):
        try:
            return Runtimeinfo.objects.filter(solution_id=obj.solution_id)[0].error
        except:
            return ""

    class Meta:
        model = Solution
        fields = ('result', 'language', 'code', 'error_msg')


class NewsSerializer(serializers.ModelSerializer):
    nick = serializers.SerializerMethodField()

    def get_nick(self, obj):
        return obj.uid.nick

    class Meta:
        model = News
        fields = ('news_id', 'uid', 'title', 'time', 'content', 'importance', 'nick', 'defunct')
