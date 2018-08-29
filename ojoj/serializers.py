from rest_framework import serializers
from django.utils import timezone
import json, datetime
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
    school_name = serializers.SerializerMethodField()

    def get_school_name(self, obj):
        if obj.school == '0':
            return "广东技术师范学院"
        schools = School.objects.filter(school_id=-1)
        try:
            school = schools.get(id=obj.school)
            return school.name
        except:
            return ""

    class Meta:
        model = Users
        fields = ('uid', 'user_id', 'nick', 'identity', 'avatarurl', 'reg_time', 'login_time',
                  'email', 'sex', 'qq', 'signature', 'school_name')


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
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        if obj.title == 'null':
            return obj.description
        else:
            return obj.title

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
    job = serializers.SerializerMethodField()

    def get_job(self, obj):
        try:
            return json.loads(obj.job)
        except:
            return ""

    class Meta:
        model = AboutUs
        fields = ('id', 'name', 'avatarurl', 'description', 'job', 'grade')


class RankUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('uid', 'nick', 'signature', 'solved', 'submit')


class QuestionTypeSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    # 1填空题  2单选题 3编程题 4问答题 5判断题
    type_dict = {1: '填空题', 2: '单选题', 3: '编程题', 4: '问答题', 5: '判断题'}

    def get_type(self, obj):
        return self.type_dict[obj.problem_type]

    class Meta:
        model = QuestionType
        fields = ('type', 'question_num', 'type_bonus')


class TemplateSerializer(serializers.ModelSerializer):
    question_type = serializers.SerializerMethodField()

    def get_question_type(self, obj):
        types = obj.questiontype_set.all().order_by('problem_type')
        return QuestionTypeSerializer(types, many=True).data

    class Meta:
        model = Template
        fields = ('template_id', 'name', 'question_type')


class ProblemTypeSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField()
    tagnames = serializers.SerializerMethodField()
    tagids = serializers.SerializerMethodField()

    def get_tagnames(self, obj):
        return [tag.tagname for tag in obj.tags.all()]

    def get_tagids(self, obj):
        return [tag.tagid for tag in obj.tags.all()]

    def get_info(self, obj):
        title = obj.title
        description = obj.description
        problem_type = obj.problem_type
        if problem_type == 1:  # 填空题
            return {'title': title, 'description': description}
        elif problem_type == 2:  # 单选题
            options = obj.sample_input.split('||')
            return {'title': title, 'description': description, 'optionA': options[0], 'optionB': options[1], 'optionC': options[2],
                    'optionD': options[3]}
        elif problem_type == 3:  # 编程题
            return {'title': title, 'description': description, 'input': obj.input, 'output': obj.output,
                    'sample_input': obj.sample_input, 'sample_output': obj.sample_output,
                    'memory_limit': obj.memory_limit, 'time_limit': obj.time_limit}
        elif problem_type == 4:  # 问答题
            return {'title': title, 'description': description}
        elif problem_type == 5:  # 判断题
            return {'title': title, 'description': description}

    class Meta:
        model = Problem
        fields = ('problem_id', 'problem_type', 'info', 'defunct', 'source', 'in_date',
                  'tagnames', 'tagids')


class QuizProblemSerializer(serializers.ModelSerializer):
    problem = serializers.SerializerMethodField()

    def get_problem(self, obj):
        problem = Problem.objects.get(problem_id=obj.problem_id)
        return ProblemTypeSerializer(problem).data

    class Meta:
        model = CoursesQuizProblem
        fields = ('item_id', 'problem_bonus', 'problem')


class QuizSerializer(serializers.ModelSerializer):
    quiz_state = serializers.SerializerMethodField()

    def get_quiz_state(self, obj):
        try:
            # 考试状态 (0.未进行 1.进行中 2.等待批阅 3.已公布成绩) 默认为0
            quiz_date = obj.quiz_date
            quiz_duration = obj.quiz_duration
            now = timezone.now()
            end = quiz_date + datetime.timedelta(minutes=int(quiz_duration))
            if now > quiz_date and now < end:
                obj.quiz_state = 1
                obj.save()
            return obj.quiz_state
        except:
            return obj.quiz_state

    class Meta:
        model = CoursesQuiz
        fields = ('quiz_id', 'quiz_name', 'quiz_manual', 'quiz_state', 'quiz_date', 'quiz_duration')


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = ('courses_id', 'courses_name', 'grade', 'term')


class ContestRankSerializer(serializers.ModelSerializer):
    nick = serializers.SerializerMethodField()

    def get_nick(self, obj):
        try:
            user = Users.objects.get(uid=obj.uid)
            return user.nick
        except:
            return ""

    class Meta:
        model = ContestFinish
        fields = ('all_time', 'uid', 'nick', 'accept_num', 'submit_num', 'finish')


class CourseExamSerializer(serializers.ModelSerializer):
    pass_student_count = serializers.SerializerMethodField()
    problem_count = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    def get_pass_student_count(self, obj):
        return Solution.objects.filter(exam_id=obj.exam_id, problem_belong=1, result=4).count()

    def get_problem_count(self, obj):
        return CoursesExamProblem.objects.filter(exam_id=obj.exam_id).count()

    def get_status(self, obj):
        stop_time = obj.stop_time
        if stop_time > timezone.now():
            return 1
        else:
            return 0

    def get_student_count(self, obj):
        course = obj.courses_id
        cls = Class.objects.filter(class_id__in=CoursesClass.objects.filter(courses_id=course).values_list('class_id', flat=True))
        student_count = 0
        for i in cls: student_count += i.studentnum
        return student_count

    class Meta:
        model = CoursesExam
        fields = ('exam_id', 'exam_name', 'create_time', 'stop_time', 'pass_student_count',
                  'problem_count', 'status', 'student_count')


class QuizDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizDetail
        fields = ('item_id', 'problem_id', 'user_answer')