from rest_framework import generics
from rest_framework.response import Response
from ..models import *
from ..serializers import CourseSerializer, CourseExamSerializer
from ..utils import get_params_from_post, data_wrapper


class CourseView(generics.GenericAPIView):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer

    def get(self, request):
        try:
            # cookie = request.session['cookie']
            # user = Users.objects.get(cookie=cookie)
            uid = request.GET['uid']
            user = Users.objects.get(uid=uid)
            if user.identity == '2':
                ct = CoursesTeacher.objects.filter(teacher_id=user.uid)
                courses = Courses.objects.filter(courses_id__in=ct.values_list('courses_id', flat=True)).order_by('courses_id')
            else:
                cc = CoursesClass.objects.filter(class_id=user.class_id)
                courses = Courses.objects.filter(courses_id__in=cc.values_list('courses_id', flat=True)).order_by('courses_id')
        except:
            return Response(data_wrapper(msg=20003, success="false"))
        data = self.get_serializer(courses, many=True).data
        return Response(data_wrapper(data=data, success="true"))

    def post(self, request):
        namedict = {'courses_name': 20001, 'grade': 20001, 'term': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            # cookie = request.session['cookie']
            # teacher = Users.objects.get(cookie=cookie)
            uid = request.POST['uid']
            teacher = Users.objects.get(uid=uid)
            course = Courses.objects.create(**params)
            course.save()
            # 存入课程教师关系表
            CoursesTeacher.objects.create(courses_id=course.courses_id, teacher_id=teacher.uid).save()
        except:
            return Response(data_wrapper(msg=20003, success="false"))
        data = self.get_serializer(course).data
        return Response(data_wrapper(data=data, success="true"))

    def delete(self, request):
        try:
            courses_id = request.GET['courses_id']
            # cookie = request.session['cookie']
            # teacher = Users.objects.get(cookie=cookie)
            uid = request.GET['uid']
            teacher = Users.objects.get(uid=uid)
            ct = CoursesTeacher.objects.filter(teacher_id=teacher.uid, courses_id=courses_id)
            if not ct.exists():
                return Response(data_wrapper(msg=20001, success="false"))
            course = self.queryset.get(courses_id=courses_id)
            course.delete()
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(success="true"))


def get_exam_data(exam, uid):
    solutions = Solution.objects.filter(uid=uid, result=4,
                    problem_id__in=CoursesExamProblem.objects.filter(exam_id=exam.exam_id).values_list('problem_id', flat=True))
    count = len(solutions.values('problem_id').distinct())
    exam_data = CourseExamSerializer(exam).data
    exam_data.update({'solved_count': count})
    return exam_data

class CourseExamView(generics.GenericAPIView):
    queryset = CoursesExam.objects.all()
    serializer_class = CourseExamSerializer

    def get(self, request):
        try:
            uid = request.GET['uid']
            courses_id = request.GET['courses_id']
            course = Courses.objects.get(courses_id=courses_id)
            exams = self.queryset.filter(courses_id=course).order_by('-exam_id')
            user = Users.objects.get(uid=uid)
            data = []
            # 获取solved_count
            for exam in exams:
                exam_data = get_exam_data(exam, user.uid)
                data.append(exam_data)
            return Response(data_wrapper(data=data, success="true"))
        except:
            return Response(data_wrapper(msg=20001, success="false"))


class ExamProblemView(generics.GenericAPIView):
    queryset = CoursesExam.objects.all()
    serializer_class = CourseExamSerializer

    def get(self, request):
        try:
            exam_id = request.GET['exam_id']
            exam = self.queryset.get(exam_id=exam_id)
            problems = Problem.objects.filter(problem_id__in=CoursesExamProblem.objects.filter(exam_id=exam.exam_id).values_list('problem_id', flat=True))

        except:
            return Response(data_wrapper(msg=20001, success="false"))