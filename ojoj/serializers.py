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
        fields = ('uid', 'user_id', 'nick', 'contact', 'code', 'academy_name', 'major_name', 'course_num',
                  'sex', 'email', 'qq')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('uid', 'user_id', 'nick', 'identity', 'avatarurl', 'reg_time', 'login_time',
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
                  'contact', 'grade')


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
                  'hastestdata', 'tagnames', 'accept_rate')


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


class FeedbackSerializer(serializers.ModelSerializer):
    identity = serializers.SerializerMethodField()
    nick = serializers.SerializerMethodField()

    def get_identity(self, obj):
        return obj.uid.identity

    def get_nick(self, obj):
        return obj.uid.nick

    class Meta:
        model = Feedback
        fields = ('fid', 'uid', 'identity', 'title', 'type', 'nick', 'is_mark', 'is_solved', 'content')


class MaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Maintenance
        fields = ('start', 'end')


class ContestSerializer(serializers.ModelSerializer):
    has_password = serializers.SerializerMethodField()

    def get_has_password(self, obj):
        if obj.password:
            return 1
        return 0

    class Meta:
        model = Contest
        fields = ('contest_id', 'begin', 'end', 'holder', 'has_password', 'score', 'state', 'title', 'type')


class ContestProblemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ('problem_id', 'accepted', 'submit', 'title')


class ContestDetailSerializer(serializers.ModelSerializer):
    contest_info = serializers.SerializerMethodField()
    problem_info = serializers.SerializerMethodField()

    def get_contest_info(self, obj):
        data = ContestSerializer(obj).data
        data['password'] = obj.password
        return data

    def get_problem_info(self, obj):
        problem_set = obj.problem_set.order_by('problem_id')
        return {'problem_list': ContestProblemSerializer(problem_set, many=True).data,
                'problem_num': problem_set.count()}

    class Meta:
        model = Contest
        fields = ('contest_info', 'problem_info')


class LabelSerilizer(serializers.ModelSerializer):
    article_num = serializers.SerializerMethodField()

    def get_article_num(self, obj):
        return ArticleLabel.objects.filter(labelid=obj).count()

    class Meta:
        model = Label
        fields = ('labelid', 'name', 'pid', 'description', 'type', 'iconUrl', 'bannerUrl', 'article_num')


class ArticleSerializer(serializers.ModelSerializer):
    avatarurl = serializers.SerializerMethodField()
    publisherid = serializers.SerializerMethodField()
    publishername = serializers.SerializerMethodField()

    def get_avatarurl(self, obj):
        return obj.publisher.avatarurl

    def get_publisherid(self, obj):
        return obj.publisher.uid

    def get_publishername(self, obj):
        return obj.publisher.nick

    class Meta:
        model = Article
        fields = ('articleid', 'title', 'agreenum', 'avatarurl', 'isMarkdown', 'isQuality', 'isTop',
                  'labelid', 'publisherid', 'publishername', 'publishtime', 'pvnum', 'summary', 'tagnames')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('tagid', 'tagname', 'pid')


class StateSerializer(serializers.ModelSerializer):
    nick = serializers.SerializerMethodField()

    def get_nick(self, obj):
        try:
            return Users.objects.get(uid=obj.uid).nick
        except:
            return ""

    class Meta:
        model = Solution
        fields = ('code_length', 'in_date', 'language', 'memory', 'nick', 'problem_id', 'protype', 'result',
                  'solution_id', 'time', 'uid')


class AboutUsSerializer(serializers.ModelSerializer):
    class_name = serializers.SerializerMethodField()

    def get_class_name(self, obj):
        try:
            cls = Class.objects.get(class_id=obj.class_id)
            return cls.class_name
        except:
            return ""

    class Meta:
        model = AboutUs
        fields = ('id', 'name', 'avatarurl', 'class_name', 'job')