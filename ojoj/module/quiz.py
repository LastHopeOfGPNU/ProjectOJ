from rest_framework import generics
from rest_framework.response import Response
import json, datetime
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
            courses_id = request.GET['courses_id']
            quiz = self.queryset.filter(courses_id=courses_id).order_by('-quiz_date')
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        data = self.serializer_class(quiz, many=True).data
        return Response(data_wrapper(data=data, success="true"))

    def get_problem_info(self, problem):
        return QuizProblemSerializer(problem).data

    def post(self, request):
        namedict = {'quiz_name': 20001, 'quiz_date': 20001, 'quiz_duration': 20001,
                    'quiz_manual': 20001, 'courses_id': 20001, 'template_id': 20001,
                    'problem_ids': 20001, 'preview': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            problem_ids = json.loads(params.pop('problem_ids'))
            template = Template.objects.get(template_id=params.pop('template_id'))
            preview = params.pop('preview', None)
            params['template'] = template
            params['quiz_date'] = datetime.datetime.strptime(params['quiz_date'], "%Y-%m-%d %H:%M:%S")
            courses_quiz = CoursesQuiz.objects.create(**params)
            courses_quiz.save()
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
            data = self.get_serializer(courses_quiz).data
            data.update({'problem_info': problem_info})
            return Response(data_wrapper(data=data, success="true"))
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        finally:
            if preview == "true":
                courses_quiz.delete()


class QuizProblemView(generics.GenericAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemTypeSerializer

    def get(self, request):
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
        except Exception as e:
            return Response(data_wrapper(msg=20001, success="false"))
        data = {
            'problems': self.get_serializer(problem_set, many=True).data,
            'total': problem_set.count()
                }
        return Response(data_wrapper(data=data, success="true"))


class QuizDetailView(generics.GenericAPIView):
    queryset = QuizDetail.objects.all()
    serializer_class = QuizDetailSerializer

    def get(self, request):
        try:
            uid = request.GET['uid']
            quiz_id = request.GET['quiz_id']
            items = self.queryset.filter(uid=uid, quiz_id=quiz_id).order_by('item_id')
            data = self.get_serializer(items, many=True).data
            return Response(data_wrapper(data=data, success="true"))
        except:
            return Response(data_wrapper(msg=20001, success="false"))