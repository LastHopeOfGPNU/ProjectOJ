from rest_framework import generics
from rest_framework.response import Response
import json, datetime
from .core import BaseListView
from .dealer import *
from ..utils import data_wrapper, get_params_from_post
from ..models import *
from ..serializers import *


class TemplateView(generics.GenericAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def get(self, request):
        uid = request.GET.get('uid', 0)
        try:
            templates = self.queryset.filter(uid=uid).order_by('template_id')
            data = self.get_serializer(templates, many=True).data
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(data=data, success="true"))

    def post(self, request):
        namedict = {'uid': 20001, 'name': 20001, 'type1_num': 20001, "type1_bonus": 20001,
                    'type2_num': 20001, "type2_bonus": 20001, 'type3_num': 20001, "type3_bonus": 20001,
                    'type4_num': 20001, "type4_bonus": 20001, 'type5_num': 20001, "type5_bonus": 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            template = Template.objects.create(uid=params['uid'], name=params['name'])
            template.save()
            for i in range(1, 6):
                question_type = QuestionType.objects.create(problem_type=i,
                                                            question_num=params['type%d_num' % i],
                                                            type_bonus=params['type%d_bonus' % i],
                                                            template_id=template.template_id)
                question_type.save()
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        data = self.get_serializer(template).data
        return Response(data_wrapper(data=data, success="true"))

    def put(self, request):
        namedict = {'template_id': 20001, 'name': 20001, 'type1_num': 20001, "type1_bonus": 20001,
                    'type2_num': 20001, "type2_bonus": 20001, 'type3_num': 20001, "type3_bonus": 20001,
                    'type4_num': 20001, "type4_bonus": 20001, 'type5_num': 20001, "type5_bonus": 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            template = self.queryset.get(template_id=params['template_id'])
            template.name = params['name']
            template.save()
            type_set = template.questiontype_set.all()
            for i in range(1, 6):
                type = type_set.get(problem_type=i)
                type.question_num = params['type%d_num' % i]
                type.type_bonus = params['type%d_bonus' % i]
                type.save()
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        data = self.get_serializer(template).data
        return Response(data_wrapper(data=data, success="true"))

    def delete(self, request):
        try:
            template_id = request.GET['template_id']
            template = self.queryset.get(template_id=template_id)
            template.delete()
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(success="true"))


class PaperView(generics.GenericAPIView):
    queryset = CoursesQuiz.objects.all()
    serializer_class = QuizSerializer

    def get(self, request):
        try:
            quiz_id = request.GET['quiz_id']
            quiz = self.queryset.get(quiz_id=quiz_id)
            data = self.get_serializer(quiz).data
            problems = quiz.coursesquizproblem_set.all().order_by('item_id')
            problem_info = QuizProblemSerializer(problems, many=True).data
            data.update({'problem_info': problem_info})
            return Response(data_wrapper(data=data, success="true"))
        except:
            return Response(data_wrapper(msg=20001, success="false"))


class QuizView(generics.GenericAPIView):
    queryset = CoursesQuiz.objects.all()
    serializer_class = QuizSerializer

    def get(self, request):
        try:
            courses_id = request.GET.get('courses_id', None)
            uid = request.GET['uid']
            user = Users.objects.get(uid=uid)
            if not courses_id:
                cc = CoursesClass.objects.filter(class_id=user.class_id)
                courses = Courses.objects.filter(courses_id__in=cc.values_list('courses_id', flat=True)).order_by('courses_id')
                quiz = self.queryset.filter(courses_id__in=courses.values_list('courses_id', flat=True)).order_by('-quiz_date')
            else:
                quiz = self.queryset.filter(courses_id=courses_id).order_by('-quiz_date')
            data = self.serializer_class(quiz, many=True).data
            return Response(data_wrapper(data=data, success="true"))
        except:
            return Response(data_wrapper(msg=20001, success="false"))

    def get_problem_info(self, problem):
        return QuizProblemSerializer(problem).data

    def post(self, request):
        namedict = {'quiz_name': 20001, 'quiz_date': 20001, 'quiz_duration': 20001,
                    'quiz_manual': 20001, 'courses_id': 20001, 'template_id': 20001,
                    'problem_ids': 20001, 'preview': 20001}
        params = get_params_from_post(request, namedict)
        # 创建deleteFlag以防删除courses_quiz时实例还没创建
        deleteFlag = False
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            problem_ids = json.loads(params.pop('problem_ids'))
            template = Template.objects.get(template_id=params.pop('template_id'))
            preview = params.pop('preview', None)
            params['template'] = template
            params['quiz_date'] = datetime.datetime.strptime(params['quiz_date'], "%Y-%m-%d %H:%M:%S")
            # 创建考试主体
            courses_quiz = CoursesQuiz.objects.create(**params)
            courses_quiz.save()
            deleteFlag = True
            # 创建考试题目（courses_quiz_problem表）
            problem_info = []
            for i, problem_id in enumerate(problem_ids):
                problem = Problem.objects.get(problem_id=problem_id)
                type = template.questiontype_set.get(problem_type=problem.problem_type)
                quiz_problem = CoursesQuizProblem.objects.create(quiz_id=courses_quiz,
                                                                problem_id=problem_id,
                                                                item_id=i+1,
                                                                problem_type=problem.problem_type,
                                                                problem_bonus=type.type_bonus/type.question_num)
                quiz_problem.save()
                problem_info.append(self.get_problem_info(quiz_problem))
            # 返回数据
            data = self.get_serializer(courses_quiz).data
            data.update({'problem_info': problem_info})
            return Response(data_wrapper(data=data, success="true"))
        except:
            if deleteFlag:
                courses_quiz.delete()
                deleteFlag = False
            return Response(data_wrapper(msg=20001, success="false"))
        finally:
            if preview == "true":
                if deleteFlag: courses_quiz.delete()


class QuizProblemView(BaseListView):
    queryset = Problem.objects.all()
    serializer_class = ProblemTypeSerializer

    def get_dataset(self, request):
        try:
            tagids = json.loads(request.GET['tagids'])
            problem_type = request.GET['problem_type']
            problem_num = request.GET.get('problem_num', None)
            dataset = self.queryset.filter(problem_type=problem_type)
            problem_set = self.queryset.none()
            for tagid in tagids:
                problems = dataset.filter(tags__tagid=tagid)
                problem_set = problem_set | problems
            problem_set = problem_set.order_by('problem_id')
            if problem_num:
                problem_num = int(problem_num)
                if problem_num < problem_set.count():
                    problem_set = problem_set.order_by('?')[:problem_num]
            return problem_set
        except:
            return self.queryset.none()


class QuizDetailView(generics.GenericAPIView):
    queryset = QuizDetail.objects.all()
    serializer_class = QuizDetailSerializer

    def get(self, request):
        # 获取用户考试每道题目答案
        # 用于保存回显
        try:
            uid = request.GET['uid']
            quiz_id = request.GET['quiz_id']
            items = self.queryset.filter(uid=uid, quiz_id=quiz_id).order_by('item_id')
            data = self.get_serializer(items, many=True).data
            return Response(data_wrapper(data=data, success="true"))
        except:
            return Response(data_wrapper(msg=20001, success="false"))

    def post(self, request):
        #namedict = {'uid': 20001, 'quiz_id': 20001, 'answers': 20001, 'submit': 20001}
        #params = get_params_from_post(request, namedict)
        #if params.pop('error'):
        #    return Response(data_wrapper(msg=20001, success="false"))
        try:
            params = json.loads(request.POST)
            answers = params['answers']  # json.loads(params.pop('answers'))
            # 判断考试是否已结束 或 学生已提交试卷
            # 考试状态 (0.未进行 1.进行中 2.等待批阅 3.已公布成绩)
            user = Users.objects.get(uid=params['uid'])
            quiz = CoursesQuiz.objects.get(quiz_id=params['quiz_id'])
            quiz_data = QuizSerializer(quiz).data
            # 通过session判断是否已提交，没有session则创建
            quiz_session = QuizSession.objects.filter(uid=user.uid, quiz_id=quiz)
            if quiz_session.exists():
                quiz_session = quiz_session[0]
            else:
                quiz_session = QuizSession.objects.create(uid=user.uid, quiz_id=quiz)
                quiz_session.save()
            if quiz_data['quiz_state'] != 1:
                return Response(data_wrapper(msg=70000, success="false"))
            if quiz_session.finished == 1:
                return Response(data_wrapper(msg=70001, success="false"))
            # 保存或提交试卷
            # 先判断之前是否已有保存
            # answers格式[item_id, problem_id, answer]
            for answer in answers:
                item_id = answer[0]
                problem_id = answer[1]
                ans = answer[2]
                record = self.queryset.filter(item_id=item_id, problem_id=problem_id)
                if not record.exists():
                    record = self.queryset.create(uid=user.uid, quiz_id=quiz.quiz_id, problem_id=problem_id, item_id=item_id)
                    record.save()
                else:
                    record = record[0]
                if record.user_answer != ans:
                    record.user_answer = ans
                    record.save()
            if params['submit'] == "true":
                quiz_session.finished = 1
                quiz_session.save()
            return Response(data_wrapper(success="true"))
        except Exception as e:
            print(e.__repr__())
            return Response(data_wrapper(msg=20001, success="false"))


class QuizAutoJudgeView(generics.GenericAPIView):
    queryset = QuizDetail.objects.all()
    serializer_class = QuizJudgeSerializer

    def get(self, request):
        try:
            quiz_id = request.GET['quiz_id']
            uid = request.GET['uid']
            quiz_detail = self.queryset.filter(uid=uid, quiz_id=quiz_id).order_by('item_id')
            judge = ProblemJudge()
            mark = 0
            for item in quiz_detail:
                problem = Problem.objects.get(problem_id=item.problem_id)
                quiz_problem = CoursesQuizProblem.objects.get(quiz_id=quiz_id, problem_id=problem.problem_id)
                result = judge.judge(item)
                # 对则满分，错则0分
                item.score = quiz_problem.problem_bonus if result else 0
                mark += item.score
                item.save()
            quiz_session = QuizSession.objects.get(uid=uid, quiz_id=quiz_id)
            quiz_session.auto_mark = mark
            quiz_session.save()
            data = self.get_serializer(quiz_detail, many=True).data
            return Response(data_wrapper(data=data, success="true"))
        except Exception as e:
            print(e.__repr__())
            return Response(data_wrapper(msg=20001, success="false"))


class QuizManualJudge(generics.GenericAPIView):
    queryset = QuizDetail.objects.all()
    serializer_class = QuizJudgeSerializer

    def get(self, request):
        try:
            quiz_id = request.GET['quiz_id']
            uid = request.GET['uid']
            quiz_detail = self.queryset.filter(uid=uid, quiz_id=quiz_id).order_by('item_id')
            data = self.get_serializer(quiz_detail, many=True).data
            return Response(data_wrapper(data=data, success="true"))
        except Exception as e:
            print(e.__repr__())
            return Response(data_wrapper(msg=20001, success="false"))

    def post(self, request):
        namedict = {'uid': 20001, 'quiz_id': 20001, 'judges': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            quiz_detail = self.queryset.filter(uid=params['uid'], quiz_id=params['quiz_id']).order_by('item_id')
            judges = json.loads(params['judges'])
            # judges格式：[item_id, score]
            for judge in judges:
                item = quiz_detail.get(item_id=judge[0])
                item.score = float(judge[1])
                item.save()
            data = self.get_serializer(quiz_detail, many=True).data
            return Response(data_wrapper(data=data, success="true"))
        except Exception as e:
            print(e.__repr__())
            return Response(data_wrapper(msg=20001, success="false"))

    def put(self, request):
        # 公布成绩
        # 是否计算成绩排名？
        namedict = {'quiz_id': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            quiz = CoursesQuiz.objects.get(quiz_id=params['quiz_id'])
            # 计算每个学生总成绩（暂不计算排名）
            quiz_session = QuizSession.objects.filter(quiz_id=params['quiz_id'])
            for session in quiz_session:
                quiz_detail = QuizDetail.objects.filter(uid=session.uid, quiz_id=params['quiz_id'])
                mark = 0
                for item in quiz_detail:
                    mark += item.score
                session.mark = mark
                session.save()
            # 更新考试状态
            quiz.quiz_state = 3
            quiz.save()
            return Response(data_wrapper(success="true"))
        except Exception as e:
            print(e.__repr__())
            return Response(data_wrapper(msg=20001, success="false"))